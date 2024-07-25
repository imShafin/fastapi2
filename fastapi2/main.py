from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from typing import List
from pydantic import BaseModel, ValidationError

# DB configuration
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Hideme@localhost/demo"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}, future=True
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI inits...
app = FastAPI()


# Models

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    courses = relationship("Course", secondary='student_course_teacher', back_populates="students")


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    courses = relationship("Course", secondary='student_course_teacher', back_populates="teachers")


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    students = relationship("Student", secondary='student_course_teacher', back_populates="courses")
    teachers = relationship("Teacher", secondary='student_course_teacher', back_populates="courses")


student_course_teacher = Table('student_course_teacher', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('teacher_id', Integer, ForeignKey('teachers.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

# Pydantic_schemas
class StudentBase(BaseModel):
    name: str

class TeacherBase(BaseModel):
    name: str

class CourseBase(BaseModel):
    name: str
    

class StudentCreate(StudentBase):
    ...

class TeacherCreate(TeacherBase):
    ...

class CourseCreate(CourseBase):
    ...

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

class Teacher(TeacherBase):
    id: int

    class Config:
        from_attributes = True

class Course(CourseBase):
    id: int
    students: List[Student] = []
    teachers: List[Teacher] = []
    
    class Config:
        from_attributes = True


try:
    StudentBase()
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    #> 'missing'


# CRUD 

@app.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(name=student.name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/", response_model=List[Student])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Student).offset(skip).limit(limit).all()

@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    return db.query(Student).filter(Student.id == student_id).first()

@app.post("/teachers/", response_model=Teacher)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    db_teacher = Teacher(name=teacher.name)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@app.get("/teachers/", response_model=List[Teacher])
def read_teachers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Teacher).offset(skip).limit(limit).all()

@app.get("/teachers/{teacher_id}", response_model=Teacher)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()

@app.post("/courses/", response_model=Course)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(name=course.name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses/", response_model=List[Course])
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Course).offset(skip).limit(limit).all()

@app.get("/courses/{course_id}", response_model=Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    return db.query(Course).filter(Course.id == course_id).first()

@app.post("/courses/{course_id}/students/{student_id}/", response_model=Course)
def enroll_student(course_id: int, student_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    student = db.query(Student).filter(Student.id == student_id).first()
    if not course or not student:
        raise HTTPException(status_code=404, detail="Course or student not found")
    course.students.append(student)
    db.commit()
    db.refresh(course)
    return course

@app.post("/courses/{course_id}/teachers/{teacher_id}/", response_model=Course)
def assign_teacher(course_id: int, teacher_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not course or not teacher:
        raise HTTPException(status_code=404, detail="Course or teacher not found")
    course.teachers.append(teacher)
    db.commit()
    db.refresh(course)
    return course

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
