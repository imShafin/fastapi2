from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated

from .. import crud, models, schemas
from ..database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix='/courses', 
    tags=['course']
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/courses/", response_model=schemas.Course)
async def create_course(course: schemas.Course, db: db_dependency):
    db_course = crud.get_course_by_name(db, name=course.name)
    if db_course:
        raise HTTPException(status_code=400, detail="Course already exist")
    return crud.create_course(db=db, course=course)


@router.get("/courses/", response_model=list[schemas.Course])
async def read_courses(db: db_dependency, skip: int = 0, limit: int = 100):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses


@router.get("/courses/{course_id}", response_model=schemas.Course)
async def read_course(course_id: int, db: db_dependency):
    db_course = crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.put("/courses/{course_id}", response_model=schemas.Course)
async def update_course(course_id: int, update: schemas.Course, db: db_dependency):
    db_update = crud.get_course(db, course_id=course_id)
    if db_update is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.query(models.Course).filter(models.Course.id == course_id).update(update.dict())
    db.commit()
    db.refresh(db_update)
    return db_update

@router.delete("/courses/{course_id}")
async def delete_course(course_id: int, db: db_dependency):
    db_course = crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.delete_course(db=db, course=db_course)
    
