from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated

from .. import crud, models, schemas
from ..database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/students', 
    tags=['student']
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=schemas.Student)
async def create_student(user: schemas.Student, db: db_dependency):
    return crud.create_student(db=db, user=user)


@router.get("/", response_model=list[schemas.Student])
async def read_students(db: db_dependency, skip: int = 0, limit: int = 100):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: db_dependency):
    student = crud.get_student(db, id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Not found")
    return student

@router.put("/{student_id}", response_model=schemas.Student)
async def update_student(student_id: int, update: schemas.Student, db: db_dependency):
    db_update = crud.get_student(db, id=student_id)
    if db_update is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.query(models.Student).filter(models.Student.id == student_id).update(update.dict())
    #for key, value in update.dict().items():
     #   setattr(db_update, key, value)
    db.commit()
    db.refresh(db_update)
    return db_update

@router.delete("/{student_id}")
async def delete_student(student_id: int, db: db_dependency):
    db_student = crud.get_student(db, user_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.delete_student(db=db, course=db_student)

