from tortoise.manager import Manager
from tortoise.queryset import QuerySet


class UserManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super(UserManager, self).get_queryset()

# https: // stackoverflow.com/questions/72380447/tortoiseorm-custom-queryset
