from fastapi import APIRouter, HTTPException

from .. import crud, models, schemas
from ..database import db_dependency

router = APIRouter(
    prefix='/teachers', 
    tags=['teacher']
)

@router.post("/", response_model=schemas.Teacher)
async def create_teacher(user: schemas.Teacher, db: db_dependency, ):
    return crud.create_teacher(db, user=user)


@router.get("/", response_model=list[schemas.Teacher])
async def read_teachers(db: db_dependency, skip: int = 0, limit: int = 100):
    teachers = crud.get_teachers(db, skip=skip, limit=limit)
    return teachers


@router.get("/{teacher_id}", response_model=schemas.Teacher)
async def read_teacher(teacher_id: int, db: db_dependency):
    teacher = crud.get_teacher(db, user_id=teacher_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Not found")
    return teacher

@router.put("/{teacher_id}", response_model=schemas.Teacher)
async def update_teacher(teacher_id: int, update: schemas.Teacher, db: db_dependency):
    db_update = crud.get_teacher(db, user_id=teacher_id)
    if db_update is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    db.query(models.Teacher).filter(models.Teacher.id == teacher_id).update(update.dict())
    db.commit()
    db.refresh(db_update)
    return db_update

@router.delete("/{teacher_id}")
async def delete_teacher(teacher_id: int, db: db_dependency):
    db_teacher = crud.get_course(db, user_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return crud.delete_teacher(db=db, teacher=db_teacher)
