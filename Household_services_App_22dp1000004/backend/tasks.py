from app import create_app
import requests
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
from celery import Celery, shared_task
from config import CeleryConfig
import os

# Initialize Flask app and Celery
flask_app = create_app()
celery = Celery(flask_app.name)
celery.config_from_object(CeleryConfig)

@shared_task
def test_task():
    print("Celery Task Executed!")
    return "Celery is working!"

# Replace with your actual credentials
GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAhacZMeo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=kyRaIUGRt3yhGVY99ey_zj1-bY5ZcvBmbSDoFs_3hgA"
EMAIL_SENDER = "22dp1000004@ds.study.iitm.ac.in"
EMAIL_PASSWORD = "kkrujxqcerihrywa"
TWILIO_ACCOUNT_SID = "AC2a63ba44bd8525540af6ba75ed572d53"
TWILIO_AUTH_TOKEN = "3141dbf5d88c01a7f5bf2695e82c3eac"
TWILIO_PHONE_NUMBER = "+18507870867"  # Twilio phone number
RECIPIENT_PHONE_NUMBER = "+917041758897"  # Receiver's phone number

from datetime import datetime, timedelta
from models import db, ServiceRequest, User
import requests
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
import os

GOOGLE_CHAT_WEBHOOK_URL = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

@shared_task
def send_reminders_for_pending_requests():
    """Check professionals with pending requests and send reminders"""
    from app import create_app
    app = create_app()
    
    with app.app_context():
        pending_requests = (
            db.session.query(ServiceRequest.professional_id, User.email, User.username)
            .join(User, ServiceRequest.professional_id == User.id)
            .filter(ServiceRequest.service_status == "Requested")
            .all()
        )

        for professional_id, email, username in pending_requests:
            reminder_message = f"Hello {username}, you have pending service requests. Please accept or reject them."
            
            # Send Google Chat Message
            send_google_chat_message(reminder_message)

            # Send Email Reminder
            send_email_reminder(email, reminder_message)

            # Send SMS Reminder
            send_sms_reminder(email, reminder_message)

    return f"Reminders sent to {len(pending_requests)} professionals."

# @shared_task
def send_google_chat_message(message):
    """Send a reminder via Google Chat"""
    # message = {"text": "Reminder: You have pending service requests to complete!"}
    payload = {"text": message}
    response = requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=payload)
    return response.status_code


# @shared_task
def send_email_reminder(to_email, message):
    """Send a reminder via email"""
    # print("EMAIL_SENDER:", os.getenv("EMAIL_SENDER"))
    # print("EMAIL_PASSWORD:", os.getenv("EMAIL_PASSWORD"))
    msg = EmailMessage()
    # msg.set_content("Reminder: You have pending service requests to complete!")
    msg.set_content(message)
    msg["Subject"] = "Service Request  Reminder"
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        return f"Email sent to {to_email}!"
    except Exception as e:
        return str(e)


# @shared_task
def send_sms_reminder(to_phone, message):
    """Send a reminder via SMS"""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            # body="Reminder: You have pending service requests to complete!",
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone,
        )
        return f"SMS sent! SID: {message.sid}"
    except Exception as e:
        return str(e)
