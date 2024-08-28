from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated

from . import crud, models, schemas
from .database import SessionLocal, engine
from . import models 
from .schemas import Student, Course, Teacher, StudentOut, CourseOut
from .api import auth, student, teacher, course, relation
from .api.auth import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/signin", status_code=status.HTTP_200_OK)
async def signin_user(user: user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authetication fail")
    return {"User": user}

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(course.router)
app.include_router(relation.router)
