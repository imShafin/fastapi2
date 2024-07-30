from sqlalchemy.orm import Session

from . import models, schemas



#user crud:

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, 
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user: schemas.User):
    db.delete(user)
    db.commit()
    return {"message": "Course deleted successfully"}


#student crud:

def get_student(db: Session, user_id: int):
    return db.query(models.Student).filter(models.Student.id == user_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student_by_email(db: Session, email: str):
    return db.query(models.Student).filter(models.Student.email == email).first()

def create_student(db: Session, user: schemas.StudentCreate):
    db_user = models.Student(
        name=user.name,
        roll=user.roll,
        department=user.department,
        session=user.session,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_student(db: Session, student: schemas.Student):
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}


#teacher crud:

def get_teacher(db: Session, user_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == user_id).first()

def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()

def get_teacher_by_email(db: Session, email: str):
    return db.query(models.Teacher).filter(models.Teacher.email == email).first()

def create_teacher(db: Session, user: schemas.TeacherCreate):
    db_user = models.Teacher(
        name=user.name,
        designation=user.designation,
        department=user.department,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_teacher(db: Session, teacher: schemas.Teacher):
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted successfully"}


#course crud:

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()

def get_course_by_name(db: Session, name: str):
    return db.query(models.Course).filter(models.Course.name == name).first()

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        name=course.name
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course: schemas.Course):
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}
