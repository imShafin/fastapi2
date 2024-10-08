from fastapi import (
            APIRouter, 
            HTTPException, 
            Depends
)                
import json

from .. import crud, models, schemas
from ..database import db_dependency
from ..check_auth import (
            token_verify_for_admin,
            token_verify_for_student,
            token_verify_for_teacher
)
from ..redis_connetion import RedisClient


router = APIRouter(
    prefix='/students', 
    tags=['student']
)

redis_client = RedisClient()

@router.get("/", response_model=list[schemas.Student])
async def read_students(db: db_dependency, token: str, skip: int = 0, limit: int = 100):
    redis_key = f"students:{skip}:{limit}"
    cached_data = redis_client.get_cache(redis_key)

    if cached_data:
        print('from redis')
        return json.loads(cached_data)
    
    students = crud.get_students(db, skip=skip, limit=limit)
    
    students_data = [schemas.Student.from_orm(student).dict() for student in students]

    redis_client.set_cache(redis_key, json.dumps(students_data), expiration=3600)
    return students

@router.get("/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: db_dependency, token: str):
    if (token_verify_for_admin(token=token) or
        token_verify_for_teacher(token=token) or 
        token_verify_for_student(token=token)
    ):
        redis_key = f"student:{student_id}"
        cached_student = redis_client.get_cache(redis_key)
        if cached_student: 
            print("From redis")
            return json.loads(cached_student)
        
        student = crud.get_student(db, id=student_id)

        if student is None:
            raise HTTPException(status_code=404, detail="Not found")
        
        student_data = schemas.Student.from_orm(student).dict()
        redis_client.set_cache(redis_key, json.dumps(student_data), expiration=3600)
        
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
        db.commit()
        db.refresh(db_update)

        redis_key = f"student:{student_id}"
        redis_client.delete_cache(redis_key)
        
        redis_client.publish_message(channel="student_updates", message=json.dumps({"action": "update", "student_id": student_id}))
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
        delete_student = crud.delete_student(db=db, student=student)

        redis_key = f"student:{student_id}"
        redis_client.delete_cache(redis_key)

        redis_client.publish_message(channel="student_updates", message=json.dumps({"action": "delete", "student_id": student_id}))
        
        return delete_student