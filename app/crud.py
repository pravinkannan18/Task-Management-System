from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(**project.dict(), user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session, user_id: int):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()

def get_project(db: Session, project_id: int, user_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id, models.Project.user_id == user_id).first()

def update_project(db: Session, project_id: int, project: schemas.ProjectCreate, user_id: int):
    db_project = get_project(db, project_id, user_id)
    if db_project:
        for key, value in project.dict().items():
            setattr(db_project, key, value)
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int, user_id: int):
    db_project = get_project(db, project_id, user_id)
    if db_project:
        db.delete(db_project)
        db.commit()
    return db_project

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
       db_task = models.Task(**task.dict())
       db.add(db_task)
       db.commit()
       db.refresh(db_task)
       return db_task

def get_tasks(db: Session, user_id: int, status: str = None, priority: int = None, due_date: datetime = None, project_id: int = None, sort_by: str = None, order: str = "asc", page: int = 1, per_page: int = 10):
    query = db.query(models.Task).join(models.Project).filter(models.Project.user_id == user_id)
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if due_date:
        query = query.filter(models.Task.due_date <= due_date)
    if project_id:
           query = query.filter(models.Task.project_id == project_id)
    if sort_by:
        order_col = getattr(models.Task, sort_by)
        query = query.order_by(order_col.asc() if order == "asc" else order_col.desc())
    return query.offset((page - 1) * per_page).limit(per_page).all()

def get_task(db: Session, task_id: int, user_id: int):
    return db.query(models.Task).join(models.Project).filter(models.Task.id == task_id, models.Project.user_id == user_id).first()

def update_task(db: Session, task_id: int, task: schemas.TaskCreate, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    db_task = get_task(db, task_id, user_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task