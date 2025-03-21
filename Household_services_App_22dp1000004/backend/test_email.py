import smtplib
from email.message import EmailMessage

EMAIL_SENDER = "22dp1000004@ds.study.iitm.ac.in"
EMAIL_PASSWORD = "kkrujxqcerihrywa"
EMAIL_RECEIVER = "vishwashah1104@gmail.com"

msg = EmailMessage()
msg.set_content("Test Email: SMTP setup is working!")
msg["Subject"] = "SMTP Test"
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
    print("✅ Email sent successfully!")
except Exception as e:
    print("❌ Error:", e)
