from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from tortoise.exceptions import IntegrityError

from application.api.auth import get_current_user
from application.db.app_models import Course, Enrollment, User, UserRole
from application.pydantic import (CreateCourse, CreateCourseResponse,
                                  EnrollCourse, EnrollCourseResponse)

router = APIRouter()


@router.post("/create-course/", response_model=CreateCourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course_data: CreateCourse,
                        current_user: User = Depends(get_current_user)) -> CreateCourseResponse:
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only teachers can create courses")

    existing_course = await Course.filter(course_code=course_data.course_code).first()
    if existing_course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course code already exists")

    try:
        new_course = await Course.create(
            course_code=course_data.course_code,
            title=course_data.title,
            description=course_data.description,
            teacher=current_user
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database integrity error")

    return CreateCourseResponse(message=f"Course {new_course.title} successfully created")


@router.post("/enroll-course/", response_model=EnrollCourseResponse, status_code=status.HTTP_201_CREATED)
async def enroll_course(enrollment_data: EnrollCourse,
                        current_user: User = Depends(get_current_user)) -> EnrollCourseResponse:
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can enroll")

    course = await Course.get_or_none(id=enrollment_data.course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # check if already enrolled
    is_enrolled = await Enrollment.filter(student_id=current_user.id, course_id=enrollment_data.course_id).exists()
    if is_enrolled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already enrolled in this course")

    # Enroll the student
    await Enrollment.create(student=current_user, course=course)

    return EnrollCourseResponse(message=f"Successfully enrolled in {course.title}")
