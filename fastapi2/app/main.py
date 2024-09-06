from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import User
from .schemas import User, UserCreate, TokenData
from .crud import create_user, get_user_by_username
from .dependencies import get_current_user, admin_required, teacher_required
from .auth import create_access_token

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/token")
async def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user is None or db_user.hashed_password != user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data={"username": user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@app.get("/admin/data")
def read_admin_data(current_user: TokenData = Depends(admin_required)):
    # Logic for admin to access all data
    return {"message": "Admin data"}

@app.get("/teacher/data")
def read_teacher_data(current_user: TokenData = Depends(teacher_required)):
    # Logic for teacher to access teacher and student data
    return {"message": "Teacher data"}

@app.get("/student/data")
def read_student_data(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != 'student':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student privileges required")
    # Logic for student to access their data
    return {"message": "Student data"}


