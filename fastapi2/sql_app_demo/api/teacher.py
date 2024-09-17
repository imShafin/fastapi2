from fastapi import APIRouter, HTTPException

from .. import crud, models, schemas
from ..database import db_dependency
from ..check_auth import (
    token_verify_for_admin,
    token_verify_for_student,
    token_verify_for_teacher
)
from ..redis_pubsub import publish

router = APIRouter(
    prefix='/teachers', 
    tags=['teacher']
)



@router.get("/", response_model=list[schemas.Teacher])
async def read_teachers(db: db_dependency, token: str, skip: int = 0, limit: int = 100):
    if (token_verify_for_teacher(token=token) or 
        token_verify_for_admin(token=token) or 
        token_verify_for_student(token=token)
    ):
        teachers = crud.get_teachers(db, skip=skip, limit=limit)
        return teachers


@router.get("/{teacher_id}", response_model=schemas.Teacher)
async def read_teacher(teacher_id: int, db: db_dependency, token: str):
    if (token_verify_for_admin(token=token) or
        token_verify_for_teacher(token=token) 
        #token_verify_for_student(token=token)
    ):    
        teacher = crud.get_teacher(db, user_id=teacher_id)
        if teacher is None:
            raise HTTPException(status_code=404, detail="Not found")
        return teacher

@router.put("/{teacher_id}", response_model=schemas.Teacher)
async def update_teacher(teacher_id: int, update: schemas.Teacher, db: db_dependency, token: str):
    if (token_verify_for_admin(token=token) or
        token_verify_for_teacher(token=token) or 
        token_verify_for_student(token=token)
    ):
        db_update = crud.get_teacher(db, user_id=teacher_id)
        if db_update is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        db.query(models.Teacher).filter(models.Teacher.id == teacher_id).update(update.dict())
        db.commit()
        db.refresh(db_update)

        await publish(channel="teacher_updates", message={"action": "update", "teacher_id": teacher_id})

        return db_update



@router.delete("/{teacher_id}")
async def delete_teacher(teacher_id: int, db: db_dependency, token: str):
    if (token_verify_for_admin(token=token) or
        token_verify_for_teacher(token=token) or 
        token_verify_for_student(token=token)
    ):
        teacher = crud.get_course(db, user_id=teacher_id)
        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        deleted_teacher = crud.delete_teacher(db=db, teacher=teacher)

        await publish(channel="teacher_updates", message={"action": "delete", "teacher_id": teacher_id})

        return {"detail": "Teacher deleted successfully"}
