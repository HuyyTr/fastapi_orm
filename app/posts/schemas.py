import json
from pydantic import BaseModel, ConfigDict

from typing import Optional, List
from datetime import datetime


# Category Schemas
class CategoryPostSchema(BaseModel):
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class CategorySchema(BaseModel):
    id: int
    name: str
    posts: List[CategoryPostSchema]
    # orm mode
    model_config = ConfigDict(from_attributes=True)


class CategoryCreataSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None


# Post schemas
class PostCategorySchema(BaseModel):
    name: str
    # orm mode
    model_config = ConfigDict(from_attributes=True)


class PostUserSchema(BaseModel):
    username: str
    # orm mode
    model_config = ConfigDict(from_attributes=True)


class PostCommentUserSchema(BaseModel):
    username: str
    # orm mode
    model_config = ConfigDict(from_attributes=True)


class PostCommentSchema(BaseModel):
    id: int
    content: str
    author: PostCommentUserSchema
    created_at: datetime
    # orm mode
    model_config = ConfigDict(from_attributes=True)


class PostTagSchema(BaseModel):
    id: int
    name: str
    # orm mode
    model_config = ConfigDict(from_attributes=True)


class PostSchema(BaseModel):
    id: int
    category: PostCategorySchema
    title: str
    slug: str
    excerpt: str
    content: str
    image: str
    author: PostUserSchema
    comments: List[PostCommentSchema]
    tags: List[PostTagSchema]
    created_at: datetime
    status: str

    # orm mode
    model_config = ConfigDict(from_attributes=True)


class PostCreateSchema(BaseModel):
    category_id: int
    user_id: int
    title: str
    excerpt: str
    content: str


class PostTagCreateSchema(BaseModel):
    id: int


class PostCommentCreateSchema(BaseModel):
    author_id: int
    content: str


class PostUpdateSchema(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None


# Tag Schemas
class TagSchema(BaseModel):
    id: int
    name: str
    # orm_mode
    model_config = ConfigDict(from_attributes=True)


class TagCreateSchema(BaseModel):
    name: str


class TagUpdateSchema(BaseModel):
    name: Optional[str] = None
