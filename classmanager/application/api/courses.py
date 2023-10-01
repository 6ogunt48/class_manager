from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from tortoise.exceptions import IntegrityError

from application.api.auth import get_current_user
from application.db.app_models import Course, User, UserRole
from application.pydantic import CreateCourse, CreateCourseResponse

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
