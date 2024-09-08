from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext #type: ignore
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError #type: ignore

from ..crud import get_user
from ..database import db_dependency
from ..models import User, RoleEnum, Student, Teacher
from ..schemas import CreateUserRequest, Token

router = APIRouter(
    prefix='/auth', 
    tags=['auth']
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
    db_user = get_user(db=db, user_id=create_user_request.id)
    if db_user:
        raise HTTPException(status_code=401, detail="User already created")
    
    create_user_model = User(
        id=create_user_request.id,
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role
    )
    db.add(create_user_model)
    db.commit()

    if create_user_request.role == 'student':
        db_student = Student(id=create_user_request.id)
        db.add(db_student)
        db.commit()
    elif create_user_request.role == 'teacher':
        db_teacher = Teacher(id=create_user_request.id)
        db.add(db_teacher)
        db.commit()
    else:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid role")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=10))
    return {'access_token': token, 'token_type': 'bearer'}


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user 

def create_access_token(
        username: str, user_id: int, role: RoleEnum, expires_delta: timedelta
    ):
    encode = {'sub': username, 'id': user_id, 'role': role.value}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {"username": username, "id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    


    def token_verify_for_admin( token):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role == "admin":
            return True
        return False

    def token_verify_for_student(token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role == "student":
            return True
        return False

    def token_verify_for_admin(token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role: str = payload.get("role")
        if role == "teacher":
            return True 
        return False
