from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///yourdatabase.db"
db = SQLAlchemy(app)

celery = Celery("tasks", broker="redis://localhost:6379/0")


class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    service_status = db.Column(db.String(20))  # requested/assigned/closed

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    gchat_webhook = db.Column(db.String(255))  # Google Chat Webhook URL

@celery.task
def send_daily_reminders():
    with app.app_context():
        pending_requests = (
            db.session.query(ServiceRequest, User)
            .join(User, ServiceRequest.professional_id == User.id)
            .filter(ServiceRequest.service_status == "requested")
            .all()
        )

        for request, professional in pending_requests:
            message = f"Reminder: You have pending service requests. Please review them."
            
            if professional.gchat_webhook:
                send_gchat_message(professional.gchat_webhook, message)

def send_gchat_message(webhook_url, message):
    headers = {"Content-Type": "application/json"}
    payload = {"text": message}
    requests.post(webhook_url, json=payload, headers=headers)
