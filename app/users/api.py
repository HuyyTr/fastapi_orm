from fastapi import APIRouter, status, HTTPException

from .models import User, Profile
from .schemas import UserSchema, UserCreateSchema, UserUpdateSchema, \
    ProfileSchema, ProfileUpdateSchema
from .utils import verify_password, hash_password

from typing import List


users_router = APIRouter(prefix="/users", tags=['users'])


@users_router.get("", response_model=List[UserSchema], status_code=status.HTTP_200_OK)
async def get_users():
    return await User.all()


@users_router.get("/{id}", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get_user(id: int):
    user = await User.get_or_none(id=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@users_router.post("", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreateSchema):
    user_in.password = hash_password(user_in.password)
    new_user = await User.create(**user_in.model_dump(exclude_unset=True))
    return new_user


@users_router.put("", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def update_user(id: int, user_in: UserUpdateSchema):
    user_to_update = await User.get_or_none(id=id)
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated_user = user_to_update.update_from_dict(
        user_in.model_dump(exclude_unset=True, exclude_none=True))
    await updated_user.save()
    return updated_user


@users_router.get("/{id}/profile", response_model=ProfileSchema, status_code=status.HTTP_200_OK)
async def get_user_profile(id: int):
    user = await User.get_or_none(id=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    profile = await Profile.get_or_none(user=user)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    await profile.fetch_related("user")
    return profile


@users_router.put("/{id}/profile", response_model=ProfileSchema, status_code=status.HTTP_201_CREATED)
async def update_user_profile(id: int, profile_in: ProfileUpdateSchema):
    user = await User.get_or_none(id=id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    profile_to_update = await Profile.get_or_none(user=user)
    if not profile_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    updated_profile = profile_to_update.update_from_dict(
        profile_in.model_dump(exclude_unset=True, exclude_none=True))
    await updated_profile.save()
    await updated_profile.fetch_related("user")
    return profile_to_update
