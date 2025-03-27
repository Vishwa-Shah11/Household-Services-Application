from app import create_app
import requests
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
from celery import Celery, shared_task
from config import CeleryConfig, cache
import os
from jinja2 import Template
from datetime import datetime
from models import db, ServiceRequest, User, Service
import csv
from utils import send_email

# Initialize Flask app and Celery
flask_app = create_app()
celery = Celery(flask_app.name)
celery.config_from_object(CeleryConfig)

@shared_task
def test_task():
    print("Celery Task Executed!")
    return "Celery is working!"

GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAhacZMeo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=kyRaIUGRt3yhGVY99ey_zj1-bY5ZcvBmbSDoFs_3hgA"
EMAIL_SENDER = "22dp1000004@ds.study.iitm.ac.in"
EMAIL_PASSWORD = "kkrujxqcerihrywa"
TWILIO_ACCOUNT_SID = "AC2a63ba44bd8525540af6ba75ed572d53"
TWILIO_AUTH_TOKEN = "3141dbf5d88c01a7f5bf2695e82c3eac"
TWILIO_PHONE_NUMBER = "+18507870867"
# RECIPIENT_PHONE_NUMBER = ""

@shared_task
def send_reminders_for_pending_requests():
    """Check professionals with pending requests and send reminders"""
    with flask_app.app_context():
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

            # uncomment below code when starting celery beat
            # Send SMS Reminder
            # send_sms_reminder(email, reminder_message)

    return f"Reminders sent to {len(pending_requests)} professionals."

def send_google_chat_message(message):
    """Send a reminder via Google Chat"""
    payload = {"text": message}
    response = requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=payload)
    return response.status_code

def send_email_reminder(to_email, message):
    """Send a reminder via email"""
    msg = EmailMessage()
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

def send_sms_reminder(to_phone, message):
    """Send a reminder via SMS"""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone,
        )
        return f"SMS sent! SID: {message.sid}"
    except Exception as e:
        return str(e)


@shared_task
def send_monthly_activity_report():
    """Generate and send a monthly activity report to customers."""
    with flask_app.app_context():  # Activate application context
        # first_day_last_month = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1)
        # last_day_last_month = datetime.now().replace(day=1) - timedelta(days=1)
        first_day_last_month = datetime.now().replace(day=1)  # First day of current month
        last_day_last_month = datetime.now()  # Today (current date)

        customers = User.query.filter_by(role="Customer").all()

        for customer in customers:
            service_requests = ServiceRequest.query.filter(
                ServiceRequest.customer_id == customer.id,
                ServiceRequest.date_of_request >= first_day_last_month,
                ServiceRequest.date_of_request <= last_day_last_month
            ).all()

            print(f"Customer: {customer.username}, Requests Found: {len(service_requests)}")
            for req in service_requests:
                print(f"Service ID: {req.id}, Name: {req.service.name}, Date: {req.date_of_request}, Status: {req.service_status}")

            report_html = generate_activity_report(customer.username, service_requests, first_day_last_month, last_day_last_month)

            send_email_report(customer.email, report_html)

    return "Monthly reports sent!"


def generate_activity_report(customer_name, service_requests, start_date, end_date):
    """Generate a styled HTML activity report for the customer."""
    template = Template("""
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <style>
            .report-container {
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
            h2 {
                text-align: center;
                margin-bottom: 20px;
                font-weight: bold;
            }
            .table {
                background: white;
            }
            th {
                background-color: #007bff !important;
                color: white !important;
                text-transform: uppercase;
            }
            td, th {
                padding: 10px;
                text-align: center;
            }
            .badge {
                font-size: 14px;
                padding: 5px 10px;
            }
        </style>
    </head>
    <body>
        <div class="report-container">
            <h2>Monthly Activity Report for <span class="fw-bold">{{ customer_name }}</span></h2>
            <p class="text-center"><strong>Report Period:</strong> {{ start_date.strftime('%B %Y') }}</p>
            <table class="table table-bordered table-striped text-center">
                <thead>
                    <tr>
                        <th>Service ID</th>
                        <th>Service Name</th>
                        <th>Date Requested</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% if service_requests %}
                        {% for req in service_requests %}
                            <tr>
                                <td>{{ req.id }}</td>
                                <td>{{ req.service.name if req.service else 'N/A' }}</td>
                                <td>{{ req.date_of_request.strftime('%Y-%m-%d') }}</td>
                                <td>
                                    {% if req.service_status == 'Closed' %}
                                        <span class="badge bg-success">Closed</span>
                                    {% elif req.service_status == 'Assigned' %}
                                        <span class="badge bg-primary">Assigned</span>
                                    {% elif req.service_status == 'Rejected' %}
                                        <span class="badge bg-danger">Rejected</span>
                                    {% elif req.service_status == 'Requested' %}
                                        <span class="badge bg-warning text-dark">Requested</span>
                                    {% else %}
                                        <span class="badge bg-secondary">N/A</span>
                                    {% endif %}
                                </td>
                            </tr>
                        {% endfor %}
                    {% else %}
                        <tr>
                            <td colspan="4">No service requests found for this period.</td>
                        </tr>
                    {% endif %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """)

    return template.render(customer_name=customer_name, service_requests=service_requests, start_date=start_date, end_date=end_date)


def send_email_report(customer_email, report_html):
    """Send the monthly activity report via email."""
    msg = EmailMessage()
    msg.set_content("Your monthly activity report is attached.")
    msg["Subject"] = "Monthly Activity Report"
    msg["From"] = EMAIL_SENDER
    msg["To"] = customer_email
    msg.add_alternative(report_html, subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Report sent to {customer_email}")
    except Exception as e:
        print(f"Failed to send report to {customer_email}: {e}")


@shared_task
def export_closed_service_requests():
    """Export closed service requests as a CSV file"""
    with flask_app.app_context():
        closed_requests = ServiceRequest.query.filter_by(service_status="Closed").all()
        
        if not closed_requests:
            return "No closed service requests to export."

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Closed_service_requests_{timestamp}.csv"
        file_path = os.path.join(flask_app.config["EXPORT_FOLDER"], filename)

        # Create CSV file
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Service ID", "Customer ID", "Professional ID", "Date of Request", "Remarks"])

            for request in closed_requests:
                writer.writerow([request.id, request.customer_id, request.professional_id, request.date_of_request, request.remarks])

        # Send email notification
        admin_email = flask_app.config["ADMIN_EMAIL"]
        subject = "Closed Service Requests Export Completed"
        body = f"The export file {filename} has been generated successfully."
        send_email(admin_email, subject, body, file_path)

        return f"Export completed: {filename}"
    

@celery.task
def refresh_service_cache():
    """Fetch latest services and update cache proactively"""
    with flask_app.app_context():  # Ensure database connection works inside Celery
        services = Service.query.all()
        service_list = [{"id": s.id, "name": s.name, "base_price": s.base_price} for s in services]
        cache.set("services_all", service_list, timeout=600)  # Store in cache for 10 minutes
        return f"Cache updated with {len(service_list)} services"