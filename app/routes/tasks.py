from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_db, get_current_user
from app.celery_config import send_task_notification
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_task = crud.create_task(db, task, current_user.id)
    if task.assigned_user_id:
        send_task_notification.delay(task.assigned_user_id, db_task.id, "assigned")
    return db_task

@router.get("/", response_model=list[schemas.Task])
def list_tasks(
    status: str = None,
    priority: int = None,
    due_date: datetime = None,
    project_id: int = None,
    sort_by: str = None,
    order: str = "asc",
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_tasks(db, current_user.id, status, priority, due_date, project_id, sort_by, order, page, per_page)

@router.get("/{id}", response_model=schemas.Task)
def get_task(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    task = crud.get_task(db, id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.patch("/{id}", response_model=schemas.Task)
def update_task(id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_task = crud.get_task(db, id, current_user.id)
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    old_status = db_task.status
    updated_task = crud.update_task(db, id, task, current_user.id)
    if task.assigned_user_id and task.assigned_user_id != db_task.assigned_user_id:
        send_task_notification.delay(task.assigned_user_id, id, "assigned")
    if task.status and task.status != old_status:
        send_task_notification.delay(updated_task.assigned_user_id, id, "status_changed")
    return updated_task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    task = crud.delete_task(db, id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")