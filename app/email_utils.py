import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_email(to_email: str, subject: str, body: str):
    """
    Send email using Gmail SMTP
    """
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    
    if not smtp_user or not smtp_password:
        print("❌ Email configuration missing. Please set SMTP_USER and SMTP_PASSWORD in .env file")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = to_email
        
        # Add body to email
        msg.attach(MIMEText(body, "plain"))
        
        # Gmail SMTP configuration
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            if smtp_use_tls:
                server.starttls()  # Enable security
            server.login(smtp_user, smtp_password)
            text = msg.as_string()
            server.sendmail(smtp_user, to_email, text)
            
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email to {to_email}: {e}")
        return False

def test_email_connection():
    """
    Test email configuration
    """
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not smtp_user or not smtp_password:
        print("❌ Email configuration missing")
        return False
        
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            print("✅ Email connection successful!")
            return True
    except Exception as e:
        print(f"❌ Email connection failed: {e}")
        print("Make sure you're using an App Password, not your regular Gmail password")
        return False