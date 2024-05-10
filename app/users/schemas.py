from pydantic import BaseModel, ConfigDict, computed_field

from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # orm mode
    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str


class UserUpdateSchema(BaseModel):
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class ProfileUserSchema(BaseModel):
    email: str
    username: str
    # orm mode
    model_config = ConfigDict(from_attributes=True)


class ProfileSchema(BaseModel):
    user: ProfileUserSchema
    avatar: str
    bio: str
    # orm mode
    model_config = ConfigDict(from_attributes=True)


class ProfileUpdateSchema(BaseModel):
    avatar: Optional[str] = None
    bio: Optional[str] = None
