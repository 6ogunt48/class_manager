from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from application.api.auth import get_current_user
from application.db.app_models import (Assignment, Enrollment, Marks,
                                       Marks_Pydantic, Submission, User,
                                       UserRole)
from application.pydantic import CreateMark, MarkCreateResponse, UpdateMark

router = APIRouter()


@router.post("/create-mark/", response_model=MarkCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_mark(mark: CreateMark, assignment_id: int, student_id: int,
                      current_user: User = Depends(get_current_user)) -> Marks_Pydantic:
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only teachers can add marks")

    # check if assignment exists
    assignment = await Assignment.get_or_none(id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")

    # Check if a student exists and is enrolled in the course
    student = await User.get_or_none(id=student_id)
    if not student or UserRole.STUDENT not in student.role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found or not a student role")

    is_enrolled = await Enrollment.filter(student_id=student_id, course_id=assignment.course_id).exists()
    if not is_enrolled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student not enrolled in the course")
    has_submitted = await Submission.filter(student_id=student_id, assignment_id=assignment_id).exists()
    if not has_submitted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student has not submitted the assignment")

    # create new mark
    new_mark = await Marks.create(
        score=mark.score,
        comments=mark.comments,
        assignment_id=assignment_id,
        student_id=student_id
    )

    mark_data = await Marks_Pydantic.from_tortoise_orm(new_mark)

    return MarkCreateResponse(message="Mark successfully Created", mark=mark_data)


@router.patch("/edit-mark/{mark_id}/", response_model=MarkCreateResponse, status_code=status.HTTP_200_OK)
async def edit_mark(
        mark_id: int,
        updated_mark: UpdateMark,
        current_user: User = Depends(get_current_user)) -> MarkCreateResponse:
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only teachers can edit marks")

    # Fetch existing mark
    mark = await Marks.get_or_none(id=mark_id)
    if not mark:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mark not found")

    # update the mark
    await Marks.filter(id=mark_id).update(**updated_mark.dict(exclude_unset=True))

    # Fetch updated mark data
    updated_mark_data = await Marks_Pydantic.from_queryset_single(Marks.get(id=mark_id))

    return MarkCreateResponse(message="Mark successfully updated", mark=updated_mark_data)


@router.get("/view-student-marks/", response_model=List[Marks_Pydantic], status_code=status.HTTP_200_OK)
async def view_student_marks(current_user: User = Depends(get_current_user)) -> List[Marks_Pydantic]:
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Fetch marks for the current student
    student_marks = await Marks.filter(student_id=current_user.id).all()

    if not student_marks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Marks Found")

    return [await Marks_Pydantic.from_tortoise_orm(mark) for mark in student_marks]


@router.get("/teacher/marks/{student_id}/", response_model=List[Marks_Pydantic], status_code=status.HTTP_200_OK)
async def get_student_marks_by_teacher(student_id: int, current_user: User = Depends(get_current_user)) -> List[Marks_Pydantic]:
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Fetch marks given by the teacher to the specified student
    marks = await Marks.filter(student_id=student_id).all()
    if not marks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No marks found")

    return [await Marks_Pydantic.from_tortoise_orm(mark) for mark in marks]
