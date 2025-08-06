from celery import Celery
from celery.schedules import crontab
import os

celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery.conf.beat_schedule = {
    "send-overdue-summary": {
        "task": "app.celery_config.send_overdue_summary",
        "schedule": crontab(hour=8, minute=0),  # Run daily at 8 AM
    },
}

@celery.task
def send_task_notification(user_id: int, task_id: int, event: str):
    from app.email_utils import send_email
    from app.database import SessionLocal
    from app.crud import get_user, get_task

    db = SessionLocal()
    try:
        user = get_user(db, user_id)
        task = get_task(db, task_id, user_id)
        if user and task:
            subject = f"Task {event}: {task.title}"
            body = f"Task '{task.title}' has been {event}."
            send_email(user.email, subject, body)
    finally:
        db.close()

@celery.task
def send_overdue_summary():
    from app.email_utils import send_email
    from app.database import SessionLocal
    from app.crud import get_tasks
    from app import models
    from datetime import datetime

    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        for user in users:
            tasks = get_tasks(db, user.id, status="pending", due_date=datetime.utcnow())
            if tasks:
                subject = "Overdue Tasks Summary"
                body = "Your overdue tasks:\n" + "\n".join([f"- {task.title} (Due: {task.due_date})" for task in tasks])
                send_email(user.email, subject, body)
    finally:
        db.close()