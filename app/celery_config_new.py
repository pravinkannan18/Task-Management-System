from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if Celery should be enabled
ENABLE_CELERY = os.getenv("ENABLE_CELERY", "false").lower() == "true"

if ENABLE_CELERY:
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
            "schedule": crontab(hour=9, minute=0),  # 9 AM daily
        },
    }
else:
    # Create a dummy celery object for when Celery is disabled
    class DummyCelery:
        def task(self, func):
            return func
    
    celery = DummyCelery()

def send_task_notification_sync(user_id: int, task_id: int, event: str):
    """Synchronous notification function for when Celery is disabled"""
    print(f"Notification: User {user_id} - Task {task_id} - Event: {event}")
    # You can add email sending logic here if needed

@celery.task
def send_task_notification(user_id: int, task_id: int, event: str):
    if not ENABLE_CELERY:
        return send_task_notification_sync(user_id, task_id, event)
    
    from app.email_utils import send_email
    from app.database import SessionLocal
    from app.crud import get_user, get_task

    db = SessionLocal()
    try:
        user = get_user(db, user_id)
        task = get_task(db, task_id, user_id)

        if user and task:
            subject = f"Task {event.replace('_', ' ').title()}: {task.title}"
            body = f"Your task '{task.title}' has been {event.replace('_', ' ')}."
            send_email(user.email, subject, body)
    finally:
        db.close()

@celery.task
def send_overdue_summary():
    if not ENABLE_CELERY:
        print("[DISABLED] Overdue summary task")
        return
        
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
