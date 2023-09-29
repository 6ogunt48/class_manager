from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "first_name" VARCHAR(50) NOT NULL,
    "last_name" VARCHAR(50) NOT NULL,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password_hash" VARCHAR(150) NOT NULL,
    "profile_picture" VARCHAR(255),
    "is_active" BOOL NOT NULL  DEFAULT True,
    "role" VARCHAR(10) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "refresh_token" TEXT,
    CONSTRAINT "uid_users_email_e7531f" UNIQUE ("email", "username")
);
CREATE INDEX IF NOT EXISTS "idx_users_usernam_266d85" ON "users" ("username");
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
COMMENT ON COLUMN "users"."role" IS 'STUDENT: student\nTEACHER: teacher';
CREATE TABLE IF NOT EXISTS "courses" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "course_code" VARCHAR(6) NOT NULL UNIQUE,
    "title" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "teacher_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_courses_course__cc4974" ON "courses" ("course_code");
CREATE TABLE IF NOT EXISTS "assignments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "due_date" TIMESTAMPTZ NOT NULL,
    "file_path" VARCHAR(255),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "course_id" INT NOT NULL REFERENCES "courses" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_assignments_title_2808e7" ON "assignments" ("title");
CREATE TABLE IF NOT EXISTS "enrollments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "date_enrolled" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "course_id" INT NOT NULL REFERENCES "courses" ("id") ON DELETE CASCADE,
    "student_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_enrollments_student_faeb87" UNIQUE ("student_id", "course_id")
);
CREATE TABLE IF NOT EXISTS "marks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "score" INT NOT NULL,
    "comments" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "assignment_id" INT NOT NULL REFERENCES "assignments" ("id") ON DELETE CASCADE,
    "student_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "content" TEXT NOT NULL,
    "date_sent" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "receiver_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "sender_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "notices" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL,
    "date_posted" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "course_id" INT NOT NULL REFERENCES "courses" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_notices_title_d77d2a" ON "notices" ("title");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
