from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.dependencies import get_db, get_current_user
# from app.celery_config import send_task_notification  # Disabled for now
from datetime import datetime
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/tasks", tags=["tasks"])

def send_email(to_email: str, subject: str, body: str):
    """Send email using Gmail SMTP"""
    try:
        # Get SMTP configuration from environment variables
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        
        if not smtp_user or not smtp_password:
            print("SMTP credentials not configured. Email not sent.")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_host, smtp_port)
        if smtp_use_tls:
            server.starttls()  # Enable security
        server.login(smtp_user, smtp_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(smtp_user, to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        return False

def send_notification_sync(user_id: int, task_id: int, event: str, db: Session):
    """Send notification with actual email functionality"""
    try:
        # Get user and task details from database
        user = db.query(models.User).filter(models.User.id == user_id).first()
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        
        if not user or not task:
            print(f"User {user_id} or Task {task_id} not found")
            return
        
        # Create email content based on event
        if event == "assigned":
            subject = f"New Task Assigned: {task.title}"
            body = f"""
Hello {user.name},

You have been assigned a new task:

Task: {task.title}
Description: {task.description or 'No description provided'}
Priority: {task.priority or 'Not set'}
Due Date: {task.due_date or 'Not set'}
Status: {task.status}

Please log in to the Task Management System to view more details.

Best regards,
Task Management System
            """
        elif event == "status_changed":
            subject = f"Task Status Updated: {task.title}"
            body = f"""
Hello {user.name},

The status of your task has been updated:

Task: {task.title}
New Status: {task.status}
Description: {task.description or 'No description provided'}
Due Date: {task.due_date or 'Not set'}

Please log in to the Task Management System to view more details.

Best regards,
Task Management System
            """
        else:
            subject = f"Task Notification: {task.title}"
            body = f"""
Hello {user.name},

There has been an update to your task:

Task: {task.title}
Event: {event.replace('_', ' ').title()}
Status: {task.status}

Please log in to the Task Management System to view more details.

Best regards,
Task Management System
            """
        
        # Send email
        success = send_email(user.email, subject, body.strip())
        
        if success:
            print(f"Notification sent successfully: User {user_id} - Task {task_id} - Event: {event}")
        else:
            print(f"Failed to send notification: User {user_id} - Task {task_id} - Event: {event}")
            
    except Exception as e:
        print(f"Error sending notification: {str(e)}")

def send_notification_sync_old(user_id: int, task_id: int, event: str):
    """Placeholder function for sending notifications without Celery"""
    print(f"Notification: User {user_id} - Task {task_id} - Event: {event}")
    # You can implement email sending here directly if needed

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_task = crud.create_task(db, task, current_user.id)
    if task.assigned_user_id:
        # Use synchronous notification with email sending
        send_notification_sync(task.assigned_user_id, db_task.id, "assigned", db)
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
        send_notification_sync(task.assigned_user_id, id, "assigned", db)
    if task.status and task.status != old_status:
        send_notification_sync(updated_task.assigned_user_id, id, "status_changed", db)
    return updated_task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    task = crud.delete_task(db, id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")