from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated

from .. import crud, models, schemas
from ..database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/relations', 
    tags=['relation']
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/students/{student_id}", response_model=schemas.StudentOut)
async def add_student_courses(student_id: int, course_id: int, db: db_dependency):
    db_student = crud.get_student_by_id(db, id=student_id)
    if not db_student:
        raise HTTPException(status_code=400, detail="Student not found")
    db_course = crud.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=400, detail="Course not found")
    data = models.StudentCourse(
        student_id=student_id,
        course_id=course_id
    )
    db.add(data)
    db.commit()
    db.refresh(data)  
    return db_student

@router.post("/teachers/{teacher_id}", response_model=schemas.TeacherOut)
async def add_teacher_courses(teacher_id: int, course_id: int, db: db_dependency):
    db_teacher = crud.get_teacher(db, user_id=teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=400, detail="Teacher not found")
    db_course = crud.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=400, detail="Course not found")
    data = models.TeacherCourse(
        teacher_id=teacher_id,
        course_id=course_id
    )
    db.add(data)
    db.commit()
    db.refresh(data)  
    return db_teacher

@router.get("/students/{student_id}/courses", response_model=List[schemas.Course])
def read_student_courses(student_id: int, db: db_dependency):
    student = crud.get_student(db, id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.courses


@router.get("/teachers/{teacher_id}/students", status_code=status.HTTP_200_OK)
def read_teacher_students(teacher_id: int, db: db_dependency):
    teacher = crud.get_teacher(db, user_id=teacher_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    courses = teacher.courses
    students = []
    for course in courses:
        students.append(course.students)
    return students