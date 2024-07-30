from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


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


