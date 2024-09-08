from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
import enum
from .database import Base

class RoleEnum(enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, unique=True, primary_key=True)
    username = Column(String)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum))

    student = relationship("Student", back_populates="user")
    teacher = relationship("Teacher", back_populates="user")


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

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    dept = Column(String, nullable=True)
    roll = Column(Integer, nullable=True)

    courses = relationship("Course",
                           secondary="student_course",
                           back_populates="students"
                           )
    user = relationship("User", back_populates="student")

class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    dept = Column(String, nullable=True)
    designation = Column(String, nullable=True)

    user = relationship("User", back_populates="teacher")
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
