from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

students_courses_teachers_relations = Table(
    "students_courses_relations", 
    Base.metadata, 
    Column('students_id', ForeignKey('students.id'), primary_key=True),
    Column('courses_id', ForeignKey('courses.id'), primary_key=True),
#    Column('teachers_id', ForeignKey('teachers.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    roll = Column(Integer, index=True)
    department = Column(String, index=True)
    session = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    courses = relationship(
        "Course", 
        secondary="students_courses_relations", 
        back_populates='students'
    )
    

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    designation = Column(String, index=True)
    department = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)

    students = relationship(
        "Student", 
        secondary="students_courses_relations", 
        back_populates='courses'
    )

