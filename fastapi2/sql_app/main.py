from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, joinedload

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#User

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



#students

@app.post("/students/", response_model=schemas.Student)
async def create_student(user: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_user = crud.get_student_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db=db, user=user)


@app.get("/students/", response_model=list[schemas.Student])
async def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students


@app.get("/students/{student_id}", response_model=schemas.Student)
async def read_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, user_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Not found")
    return student

@app.put("/students/{student_id}", response_model=schemas.Student)
async def update_student(student_id: int, update: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_update = crud.get_student(db, user_id=student_id)
    if db_update is None:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in update.dict().items():
        if value is not None: setattr(db_update, key, value)
    db.commit()
    return db_update

@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, user_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.delete_student(db=db, course=db_student)


#teacher

@app.post("/teachers/", response_model=schemas.Teacher)
async def create_teacher(user: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_user = crud.get_teacher_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_teacher(db=db, user=user)


@app.get("/teachers/", response_model=list[schemas.Teacher])
async def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teachers = crud.get_teachers(db, skip=skip, limit=limit)
    return teachers


@app.get("/teachers/{teacher_id}", response_model=schemas.Teacher)
async def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = crud.get_teacher(db, user_id=teacher_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Not found")
    return teacher

@app.put("/teachers/{teacher_id}", response_model=schemas.Teacher)
async def update_course(teacher_id: int, update: schemas.TeacherCreate, db: Session = Depends(get_db)):
    db_update = crud.get_course(db, user_id=teacher_id)
    if db_update is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    for key, value in update.dict().items():
        setattr(db_update, key, value)
    db.commit()
    return db_update

@app.delete("/teachers/{teacher_id}")
async def delete_course(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.get_course(db, user_id=teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return crud.delete_teacher(db=db, teacher=db_teacher)


#course

@app.post("/courses/", response_model=schemas.Course)
async def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_name(db, name=course.name)
    if db_course:
        raise HTTPException(status_code=400, detail="Course already exist")
    return crud.create_course(db=db, course=course)


@app.get("/courses/", response_model=list[schemas.Course])
async def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses


@app.get("/courses/{course_id}", response_model=schemas.Course)
async def read_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@app.put("/courses/{course_id}", response_model=schemas.Course)
async def update_course(course_id: int, update: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_update = crud.get_course(db, course_id=course_id)
    if db_update is None:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in update.items():
        setattr(db_update, key, value)
    db.commit()
    return db_update

@app.delete("/courses/{course_id}")
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.delete_course(db=db, course=db_course)
    
 

#students_courses_relations:

@app.put("/students/{id}", response_model=schemas.StudentSchema)
async def create_student_courses(id: int, courses: schemas.StudentSchema, db: Session = Depends(get_db)):
    db_user = crud.get_student(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Student not found")
    for key, value in courses.items():
        setattr(db_user.courses, key, value)
    db.commit()
    return {"message": "added"}

@app.get("/students/{id}", response_model=schemas.Student)
async def get_students(id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).options(joinedload(models.Student.courses)).\
        where(models.Student.id == id).one()
    return db_student
