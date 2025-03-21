import requests
# from celery_config import celery
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from models import db, User, ServiceRequest  # Import models

# Google Chat Webhook URL
GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAhacZMeo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=kyRaIUGRt3yhGVY99ey_zj1-bY5ZcvBmbSDoFs_3hgA"

# Twilio SMS Configuration
TWILIO_ACCOUNT_SID = "AC2a63ba44bd8525540af6ba75ed572d53"
TWILIO_AUTH_TOKEN = "3141dbf5d88c01a7f5bf2695e82c3eac"
TWILIO_PHONE_NUMBER = "+18507870867"

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "22dp1000004@ds.study.iitm.ac.in"
EMAIL_PASS = "jnuk1302@iitm"

# @celery.task
def send_daily_reminders():
    """Send daily reminders to professionals about pending service requests."""
    
    today = datetime.utcnow()
    pending_requests = ServiceRequest.query.filter(
        ServiceRequest.service_status == "requested",
        ServiceRequest.date_of_request <= today
    ).all()

    for request in pending_requests:
        professional = User.query.get(request.professional_id)
        if professional and not professional.is_blocked:
            message = f"Reminder: You have a pending service request (ID: {request.id}). Please respond."

            # Send Google Chat Notification
            send_google_chat_message(professional.email, message)

            # Send Message
            send_msg(professional.phone, message)

            # Send Email
            send_email(professional.email, "Service Reminder", message)

    return f"Sent reminders for {len(pending_requests)} requests."

def send_google_chat_message(email, message):
    """Send a message to Google Chat using Webhooks."""
    payload = {
        "text": f"@{email} {message}"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=payload, headers=headers)
    if response.status_code == 200:
        print("Message sent to Google Chat successfully.")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")
    return response.status_code

from twilio.rest import Client
def send_msg(phone, message):
    """Send SMS using Twilio."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    print(f"SMS sent to {phone}, Message SID: {message.sid}")
    return message.sid

import smtplib
from email.mime.text import MIMEText
def send_email(to_email, subject, body):
    """Send email notification."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
        return f"Email sent to {to_email}"
    except Exception as e:
        return str(e)
