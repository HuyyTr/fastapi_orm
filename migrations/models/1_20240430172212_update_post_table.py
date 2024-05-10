from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "comment" ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "post" ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "post" ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "user" ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "comment" ALTER COLUMN "created_at" SET DEFAULT CURRENT_TIMESTAMP;"""
