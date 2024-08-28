from sqlalchemy.orm import Session

from . import models, schemas



#student crud:

def get_student(db: Session, id: int):
    return db.query(models.Student).filter(models.Student.id == id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student_by_id(db: Session, id: int):
    return db.query(models.Student).filter(models.Student.id == id).first()

def create_student(db: Session, user: schemas.Student):
    db_user = models.Student(
        id=user.id,
        name=user.name,
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

def create_teacher(db: Session, user: schemas.Teacher):
    db_user = models.Teacher(
        id=user.id,
        name=user.name,
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

def create_course(db: Session, course: schemas.Course):
    db_course = models.Course(
        id=course.id,
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


def add_courses(db: Session, id: int, user: schemas.Course):
    db_user = models.StudentCourse(
        student_id = id,
        course_id = user.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user