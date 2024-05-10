from tortoise import fields, Tortoise
from tortoise.models import Model

from datetime import datetime, timezone


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, null=False, unique=True)
    username = fields.CharField(max_length=255, null=False, unique=True)
    password = fields.CharField(max_length=255, null=False)
    first_name = fields.CharField(max_length=255, null=False)
    last_name = fields.CharField(max_length=255, null=False)
    is_verified = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(
        auto_now_add=True, default=datetime.now(timezone.utc))

    class Meta:
        table = "user"


class Profile(Model):
    avatar = fields.CharField(max_length=255, null=True, default="default.ipg")
    bio = fields.TextField(max_length=255, null=True)
    user: fields.OneToOneRelation[User] = fields.OneToOneField(
        "models.User", on_delete=fields.CASCADE, related_name="profile")

    class Meta:
        table = "user_profile"
