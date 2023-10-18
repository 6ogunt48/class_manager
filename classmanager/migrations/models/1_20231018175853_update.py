from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "submissions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "file_path" VARCHAR(255),
    "submitted_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "assignment_id" INT NOT NULL REFERENCES "assignments" ("id") ON DELETE CASCADE,
    "student_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_submissions_student_8f7657" UNIQUE ("student_id", "assignment_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "submissions";"""
