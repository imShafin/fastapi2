from fastapi import FastAPI, HTTPException, status, Depends
from typing import List, Annotated
import asyncio

from .database import db_dependency
from .api import auth, student, teacher, course, relation
from .api.auth import get_current_user
from .redis_pubsub import subscribe

app = FastAPI()
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/signin", status_code=status.HTTP_200_OK)
async def signin_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authetication fail")
    return {"User": user}

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(course.router)
app.include_router(relation.router)




async def handle_redis_messages():
    student_channel = await subscribe("student_updates")
    teacher_channel = await subscribe("teacher_updates")

    while True:
        student_message = await student_channel.get_message(ignore_subscribe_messages=True)
        if student_message:
            print(f"Student Update Received: {student_message['data']}")

        teacher_message = await teacher_channel.get_message(ignore_subscribe_messages=True)
        if teacher_message:
            print(f"Teacher Update Received: {teacher_message['data']}")
        
        await asyncio.sleep(0.1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(handle_redis_messages())
