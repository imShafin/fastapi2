from fastapi import APIRouter, HTTPException
from sqlalchemy.orm.bulk_persistence import _bulk_update
from typing import Annotated
from jose import jwt #type: ignore

from .. import crud, models, schemas
from ..database import db_dependency
from ..check_auth import (
    token_verify_for_admin,
    token_verify_for_student,
    token_verify_for_teacher
    )

router = APIRouter(
    prefix='/students', 
    tags=['student']
)

@router.get("/", response_model=list[schemas.Student])
async def read_students(db: db_dependency, token: str, skip: int = 0, limit: int = 100):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: db_dependency, token: str):
    if (token_verify_for_admin(token=token) or
        token_verify_for_teacher(token=token) or 
        token_verify_for_student(token=token)
    ):
        student = crud.get_student(db, id=student_id)
        if student is None:
            raise HTTPException(status_code=404, detail="Not found")
        return student

@router.put("/{student_id}", response_model=schemas.Student)
async def update_student(student_id: int, update: schemas.Student, db: db_dependency, token: str):
    if (token_verify_for_admin(token=token) or
        #token_verify_for_teacher(token=token) or 
        token_verify_for_student(token=token)
    ):
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
async def delete_student(student_id: int, db: db_dependency, token: str):
    if (token_verify_for_admin(token=token) or
        #token_verify_for_teacher(token=token) or 
        token_verify_for_student(token=token)
    ):
        student = crud.get_student(db, id=student_id)
        if student is None:
            raise HTTPException(status_code=404, detail="Course not found")
        return crud.delete_student(db=db, student=student)

