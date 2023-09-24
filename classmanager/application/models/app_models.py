from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from enum import Enum


class UserRole(str, Enum):
    STUDENT = 'student'
    TEACHER = 'teacher'


class User(models.Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    username = fields.CharField(fields.CharField(max_length=50, unique=True, index=True))
    email = fields.CharField(max_length=100, unique=True, index=True)
    password_hash = fields.CharField(max_length=150)
    profile_picture = fields.CharField(max_length=255, null=True)
    is_active = fields.BooleanField(default=True)
    role = fields.CharEnumField(UserRole, max_length=10)

    courses = fields.ManyToManyField('models.Course', related_name='students', through='enrollments')

    class Meta:
        table = "users"
        unique_together = ("email", "username")

    def __str__(self):
        return f"{self.username} ({self.role})"


class Course(models.Model):
    id = fields.IntField(pk=True)
    course_code = fields.CharField(max_length=6, unique=True, index=True)
    title = fields.CharField(max_length=100)
    description = fields.TextField(null=True)

    teacher = fields.ForeignKeyField('models.User', related_name='courses_taught')

    class Meta:
        table = "courses"

    def __str__(self):
        return self.title


class Assignment(models.Model):
    id = fields.IntField(pk=True)
    course = fields.ForeignKeyField("models.Course", related_name="assignments")
    title = fields.CharField(max_length=100, index=True)
    description = fields.TextField()
    due_date = fields.DatetimeField()
    file_path = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "assignments"

    def __str__(self):
        return self.title


class Marks(models.Model):
    id = fields.IntField(pk=True)
    score = fields.IntField()
    comments = fields.TextField(null=True)
    student = fields.ForeignKeyField("models.User", related_name="marks")
    assignment = fields.ForeignKeyField("models.Assignment")

    class Meta:
        table = "marks"

    def __str__(self):
        return f"{self.score} for {self.assignment}"