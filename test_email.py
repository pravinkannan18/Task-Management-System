"""
Test Email Configuration Script

This script tests your Gmail SMTP configuration.
Run this after setting up your App Password.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.email_utils import test_email_connection, send_email

def main():
    print("🧪 Testing Email Configuration...")
    print("=" * 40)
    
    # Test connection
    if test_email_connection():
        print("\n📧 Sending test email...")
        
        # Send test email to yourself
        from dotenv import load_dotenv
        load_dotenv()
        
        test_email = os.getenv("SMTP_USER")
        success = send_email(
            to_email=test_email,
            subject="Task Management API - Test Email",
            body="This is a test email from your Task Management API. If you receive this, your email configuration is working correctly!"
        )
        
        if success:
            print(f"🎉 Test email sent to {test_email}")
            print("Check your inbox!")
        else:
            print("❌ Failed to send test email")
    else:
        print("\n📋 To fix email issues:")
        print("1. Make sure 2-Factor Authentication is enabled on your Google account")
        print("2. Generate an App Password at: https://myaccount.google.com/apppasswords")
        print("3. Update SMTP_PASSWORD in .env file with the 16-character App Password")
        print("4. Don't use your regular Gmail password")

if __name__ == "__main__":
    main()
