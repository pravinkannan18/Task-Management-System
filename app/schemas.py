from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models import TaskStatus

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
    confirm_password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    priority: int
    due_date: Optional[datetime] = None
    project_id: int
    assigned_user_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True