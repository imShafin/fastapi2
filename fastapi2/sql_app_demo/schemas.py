from pydantic import BaseModel
from typing import List

class Student(BaseModel):
    name: str | None 
    email: str | None 
    dept: str | None 
    roll: int | None 
    
    class Config:
        from_attribute = True

class Teacher(BaseModel):
    name: str | None  
    email: str | None 
    dept: str | None 
    designation: str | None 

    class Config:
        from_attribute = True

class Course(BaseModel):
    id: int | None  
    name: str | None  

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
    id: int
    username: str
    role: str
    password: str

    class config: 
        from_attribute = True 

class Token(BaseModel):
    access_token: str
    token_type: str

