from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    role = Column(Integer)
    hashed_password = Column(String)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

class StudentCourse(Base):
    __tablename__ = "student_course"

    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)

class TeacherCourse(Base):
    __tablename__ = "teacher_course"

    teacher_id = Column(Integer, ForeignKey("teacher.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("course.id"), primary_key=True)


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    courses = relationship("Course",
                           secondary="student_course",
                           back_populates="students"
                )

class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    courses = relationship("Course", 
                           secondary="teacher_course", 
                           back_populates="teachers"
                           )


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    students = relationship("Student",
                            secondary="student_course",
                            back_populates="courses"
                            )
    teachers = relationship("Teacher", 
                            secondary="teacher_course", 
                            back_populates="courses"
                            )
