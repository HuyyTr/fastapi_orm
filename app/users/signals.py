from tortoise.signals import post_save
from tortoise import BaseDBAsyncClient

from . models import User, Profile

from typing import List, Type

# https: // stackoverflow.com/questions/72861303/register-tortoise-signals-in -fast-api


@post_save(User)
async def crate_user_profile(
    sender: Type[User],
    instance: User,
    created: bool,
    using_db: BaseDBAsyncClient,
    update_fields: List[str]
) -> None:
    if created:
        profile = await Profile.create(user=instance)
        await profile.save()


# https://stackoverflow.com/questions/72861303/register-tortoise-signals-in-fast-api
