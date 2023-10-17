from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from application.api.auth import get_current_user
from application.db.app_models import User
from application.pydantic import UserProfile, UserProfileUpdate

router = APIRouter()


@router.get("/", response_model=UserProfile, status_code=status.HTTP_200_OK)
async def get_user_profile(current_user: User = Depends(get_current_user)) -> UserProfile:
    user_profile = await User.filter(id=current_user.id).first()
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserProfile(
        first_name=user_profile.first_name,
        last_name=user_profile.last_name,
        username=user_profile.username,
        email=user_profile.email,
        role=user_profile.role,
        created_at=user_profile.created_at,
        updated_at=user_profile.updated_at,
        profile_picture=user_profile.profile_picture
    )


@router.patch("/{user_id}/profile", response_model=UserProfile, status_code=status.HTTP_200_OK)
async def update_user_profile(user_data: UserProfileUpdate,
                              user_id: int = Path(..., title="The ID  of the user to update"),
                              current_user: User = Depends(get_current_user)) -> UserProfile:
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Get the user record
    user = await User.filter(id=user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Update the user profile fields
    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.username = user_data.username
    user.email = user_data.email
    user.role = user_data.role
    user.profile_picture = user_data.profile_picture

    # Update the 'updated_at' field with the current datetime
    user.updated_at = datetime.utcnow()  # Assuming you are using UTC time

    # Save the changes to the database
    await user.save()

    return UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
        profile_picture=user.profile_picture
    )
