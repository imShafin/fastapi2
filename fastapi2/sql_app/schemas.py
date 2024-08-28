from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserItemsBase(BaseModel):
    name: Optional[str]
    department: Optional[str]
    email: Optional[str]

class StudentCreate(UserItemsBase):
    roll: Optional[int]
    session: Optional[str] 

class Student(UserItemsBase):
    id: int

    class config:
        orm_mode = True

class TeacherCreate(UserItemsBase):
    designation: Optional[str]

class Teacher(UserItemsBase):
    id: int

    class config:
        orm_mode = True

class CourseCreate(BaseModel):
    name: Optional[str]

class Course(CourseCreate):
    id: int 

    class config:
        orm_mode = True

class CourseSchema(Course):
    students: List[Student]


class StudentSchema(Student):
    courses: List[Course]