from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "is_verified" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "user_profile" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "avatar" VARCHAR(255)   DEFAULT 'default.ipg',
    "bio" TEXT,
    "user_id" INT NOT NULL UNIQUE REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS "post" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(250) NOT NULL,
    "slug" VARCHAR(250) NOT NULL,
    "excerpt" TEXT,
    "content" TEXT NOT NULL,
    "image" VARCHAR(250)   DEFAULT 'no_image.jpg',
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(9) NOT NULL  DEFAULT 'published',
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE RESTRICT
);
COMMENT ON COLUMN "post"."status" IS 'DRAFT: draft\nPUBLISHED: published';
CREATE TABLE IF NOT EXISTS "comment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "tag" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "post_tag" (
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "tag_id" INT NOT NULL REFERENCES "tag" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
