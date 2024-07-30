from pydantic import BaseModel

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
    name: str | None
    department: str | None
    email: str | None

class StudentCreate(UserItemsBase):
    roll: int | None 
    session: str | None 

class Student(UserItemsBase):
    id: int

    class config:
        orm_mode = True

class TeacherCreate(UserItemsBase):
    designation: str | None

class Teacher(UserItemsBase):
    id: int

    class config:
        orm_mode = True

class CourseCreate(BaseModel):
    name: str | None

class Course(CourseCreate):
    id: int 

    class config:
        orm_mode = True
    