from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from tortoise.exceptions import IntegrityError

from application.api.auth import get_current_user
from application.db.app_models import (Assignment, Enrollment, Submission,
                                       User, UserRole)
from application.pydantic import (AssignmentCreate, AssignmentCreateResponse,
                                  CustomAssignment_Pydantic, SubmissionCreate)

router = APIRouter()


@router.post("/create-assignment/", response_model=AssignmentCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(assignment: AssignmentCreate,
                            current_user: User = Depends(get_current_user)) -> AssignmentCreateResponse:
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can create courses")

    # Check if assignment with the same title or description already exists
    existing_assignment = await Assignment.filter(title=assignment.title).first()
    if existing_assignment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assignment title already exists")

    try:
        new_assignment = await Assignment.create(
            course_id=assignment.course_id,
            title=assignment.title,
            description=assignment.description,
            due_date=assignment.due_date,
            file_path=assignment.file_path
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database Integrity error")

    return AssignmentCreateResponse(message=f"Assignment created successfully, title: {new_assignment.title}")


@router.get("/teacher/assignments", response_model=List[CustomAssignment_Pydantic], status_code=status.HTTP_200_OK)
async def get_teacher_assignments(current_user: User = Depends(get_current_user)) -> List[AssignmentCreate]:
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Fetch assignments taught by current teacher
    assignments = await Assignment.filter(course__teacher_id=current_user.id).all()

    if not assignments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No assignments found")

    return [CustomAssignment_Pydantic.from_orm(assignment) for assignment in assignments]


@router.get("/student/assignments/{course_id}", response_model=List[CustomAssignment_Pydantic],
            status_code=status.HTTP_200_OK)
async def get_student_assignments_for_a_course(course_id: int, current_user: User = Depends(get_current_user)) -> List[CustomAssignment_Pydantic]:
    # check for a student role
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Check if the student is actually enrolled in the course
    await Enrollment.filter(student_id=current_user.id, course_id=course_id).exists()

    # Fetch assignments for the course
    assignments = await Assignment.filter(course__id=course_id).all()
    if not assignments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No assignments found for this course")

    return [CustomAssignment_Pydantic.from_orm(assignment) for assignment in assignments]


@router.post("/student/submit-assignment/", status_code=status.HTTP_201_CREATED)
async def submit_assignment(submission_data: SubmissionCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # validate if the assignment exists
    assignment = await Assignment.get_or_none(id=submission_data.assignment_id)

    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")

    # validate if a student is enrolled in the course of th assignment
    is_enrolled = await Enrollment.filter(student_id=current_user.id, course_id=assignment.course_id).exists()
    if not is_enrolled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enrolled in this course")

    # Create the submission
    new_submission = await Submission.create(
        student_id=current_user.id,
        assignment_id=submission_data.assignment_id,
        file_path=submission_data.file_path
    )

    return {"message": f"Successfully, submitted assignment {new_submission.id}"}
