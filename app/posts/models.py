from tortoise import fields
from tortoise.models import Model

from datetime import datetime, timezone
from enum import Enum


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)

    posts: fields.ForeignKeyRelation["Post"]

    class Meta:
        table = "category"


class PostStatusEnum(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class Post(Model):
    id = fields.IntField(pk=True)
    category = fields.ForeignKeyField(
        "models.Category", on_delete=fields.RESTRICT, related_name="posts")
    title = fields.CharField(max_length=250)
    slug = fields.CharField(max_length=250)
    excerpt = fields.TextField(null=True)
    content = fields.TextField(null=False)
    image = fields.CharField(max_length=250, null=True, default="no_image.jpg")
    author = fields.ForeignKeyField(
        "models.User", on_delete=fields.CASCADE, related_name="posts")
    tags = fields.ManyToManyField(
        "models.Tag", related_name="posts", null=True)
    created_at = fields.DatetimeField(
        auto_now_add=True, default=datetime.now(timezone.utc))
    status = fields.CharEnumField(
        enum_type=PostStatusEnum, default="published")

    comments: fields.ReverseRelation["Comment"]

    class Meta:
        table = "post"
        ordering = ("created_at",)


class Comment(Model):
    id = fields.IntField(pk=True)
    post = fields.ForeignKeyField(
        "models.Post", on_delete=fields.CASCADE, related_name="comments")
    author = fields.ForeignKeyField(
        "models.User", on_delete=fields.CASCADE, related_name="comments")
    content = fields.TextField()
    created_at = fields.DatetimeField(
        auto_now_add=True, default=datetime.now(timezone.utc))

    class Meta:
        table = "comment"
        ordering = ("created_at",)


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

    posts: fields.ManyToManyRelation[Post]

    class Meta:
        table = "tag"
