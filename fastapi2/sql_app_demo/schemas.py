from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    id: int | None = None
    name: str | None = None

    class Config:
        from_attribute = True

class Teacher(BaseModel):
    id: int | None = None
    name: str | None = None 

    class Config:
        from_attribute = True

class Course(BaseModel):
    id: int | None = None 
    name: str | None = None 

    class Config:
        from_attribute = True


class StudentOut(Student):
    courses: List[Course]


class CourseOut(Course):
    students: List[Student]

class StudentCourse(BaseModel):
    student_id: int
    course_id: int 

    class Config:
        from_attribute = True


class TeacherOut(Teacher):
    courses: List[Course]


class CreateUserRequest(BaseModel):
    username: str
    role: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

