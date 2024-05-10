from fastapi import APIRouter, status, HTTPException
from fastapi_cache.decorator import cache


from app.users.models import User

from .models import Category, Post, Comment, Tag
from .schemas import CategorySchema, CategoryCreataSchema, CategoryUpdateSchema, \
    PostSchema, PostCreateSchema, PostUpdateSchema, PostTagCreateSchema, PostCommentCreateSchema, \
    TagSchema, TagCreateSchema, TagUpdateSchema

from .utils import slugify

from typing import List


posts_router = APIRouter(prefix="/posts", tags=["posts"])


# --------------------- category_api---------------------------
@posts_router.get("/category", response_model=List[CategorySchema], status_code=status.HTTP_200_OK)
async def get_categories():
    return await Category.all().prefetch_related('posts')


@posts_router.post("/category", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category_in: CategoryCreataSchema):
    new_category = await Category.create(**category_in.model_dump())
    return new_category


@posts_router.put("/category/{id}", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def update_category(id: int, category_in: CategoryUpdateSchema):
    category_to_update = await Category.get_or_none(id=id)
    if not category_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    updated_category = category_to_update.update_from_dict(
        category_in.model_dump(exclude_unset=True, exclude_none=True))
    await updated_category.save()
    return updated_category


# --------------------- tag_api---------------------------
@posts_router.get("/tag", response_model=List[TagSchema], status_code=status.HTTP_200_OK)
async def get_tags():
    return await Tag.all()


@posts_router.post("/tag", response_model=TagSchema, status_code=status.HTTP_201_CREATED)
async def create_tag(tag_in: TagCreateSchema):
    new_tag = await Tag.create(**tag_in.model_dump())
    return new_tag


@posts_router.put("/tag/{id}", response_model=TagSchema, status_code=status.HTTP_200_OK)
async def update_tag(id: int, tag_in: TagUpdateSchema):
    tag_to_update = await Tag.get_or_none(id=id)
    if not tag_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    updated_tag = tag_to_update.update_from_dict(
        tag_in.model_dump(exclude_unset=True, exclude_none=True))
    await updated_tag.save()
    return updated_tag


# --------------------- post_api---------------------------
@posts_router.get("", response_model=List[PostSchema], status_code=status.HTTP_200_OK)
@cache(expire=60*15)
async def get_posts():
    return await Post.all().prefetch_related("category", "author", "tags", "comments__author")


@posts_router.get("/{id}", response_model=PostSchema, status_code=status.HTTP_200_OK)
@cache(expire=60*15)
async def get_post(id: int):
    post = await Post.get_or_none(id=id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await post.fetch_related("category", "author", "tags", "comments__author")
    return post


@posts_router.post("", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(post_in: PostCreateSchema):
    category = await Category.get_or_none(id=post_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    user = await User.get_or_none(id=post_in.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    new_post = await Post.create(
        category_id=post_in.category_id,
        author_id=post_in.user_id,
        title=post_in.title,
        slug=slugify(post_in.title),
        excerpt=post_in.excerpt,
        content=post_in.content,
    )
    await new_post.fetch_related("category", "author", "tags", "comments__author")
    return new_post


@posts_router.put("/{id}", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def update_post(id: int, post_in: PostUpdateSchema):
    post_to_update = await Post.get_or_none(id=id)
    if not post_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    updated_post = post_to_update.update_from_dict(
        post_in.model_dump(exclude_unset=True, exclude_none=True))
    await updated_post.save()
    await updated_post.fetch_related("category", "author", "tags", "comments__author")
    return updated_post


@posts_router.post("/{id}/tag", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def add_tag_to_post(id: int, tag_in: PostTagCreateSchema):
    post = await Post.get_or_none(id=id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    tag = await Tag.get_or_none(id=tag_in.id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    await post.tags.add(tag)
    await post.save()
    await post.fetch_related("category", "author", "tags", "comments__author")
    return post


@posts_router.post("/{id}/comment", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def add_comment_to_post(id: int, comment_in: PostCommentCreateSchema):
    post = await Post.get_or_none(id=id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    user = await User.get_or_none(id=comment_in.author_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    await Comment.create(post_id=id, author_id=comment_in.author_id, content=comment_in.content)
    await post.fetch_related("category", "author", "tags", "comments__author")
    return post
