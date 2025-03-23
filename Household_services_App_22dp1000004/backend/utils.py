from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
import jwt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] != required_role:
                return jsonify({'message': 'Access forbidden: insufficient permissions'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_customer_id_from_token(token):
    try:
        secret_key = "your_jwt_secret_key"  # Replace with your actual secret key
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        # print("Decoded Token:", decoded_token)
        # Extract user ID from 'sub'
        user_data = decoded_token.get("sub")  # sub contains {"id": 2, "role": "Customer"}
        if not user_data or "id" not in user_data:
            print("User ID not found in token")
            return None

        customer_id = user_data["id"]
        # print(f"Found Customer ID: {customer_id}")
        return customer_id
    except jwt.ExpiredSignatureError:
        print("Token Expired")
        return None  # Token expired
    except jwt.InvalidTokenError as e:
        print(f"Invalid Token: {e}")
        return None  # Invalid token
    
def send_email(to_email, subject, body, attachment_path=None):
    """Send an email with an optional attachment"""
    sender_email = "22dp1000004@ds.study.iitm.ac.in"  # Change to your email
    sender_password = "kkrujxqcerihrywa"  # Use an app password if needed

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Attach file if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
            msg.attach(part)

    try:
        # SMTP Configuration (Gmail Example)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")