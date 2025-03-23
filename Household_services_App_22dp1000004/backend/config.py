import os
from datetime import timedelta
from celery.schedules import crontab

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///household_services.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

     # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')  # Use a secure key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)  # Increase access token expiration
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7) # Increase refresh token expiration

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    EXPORT_FOLDER = os.path.join(BASE_DIR, "exports")
    ADMIN_EMAIL = "admin@gmail.com"

    # Redis Configuration for Caching
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")  # Read from env or default to localhost
    CACHE_REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
    CACHE_DEFAULT_TIMEOUT = 300  # Cache expiry: 5 minutes

class CeleryConfig:
    # REDIS_URL = "redis://localhost:6379/0"
    REDIS_HOST = "172.22.102.218"
    REDIS_PORT = "6379"
    broker_url  = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    result_backend  = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    timezone = "Asia/Kolkata"
    broker_connection_retry_on_startup = True
    beat_schedule = {
        # 'send-reminder-every-evening': {
        #     'task': 'tasks.send_email_reminder',
        #     'schedule': crontab(hour=18, minute=0),  # Runs daily at 6 PM IST
        # },
        # 'send-gchat-reminder': {
        #     'task': 'tasks.send_google_chat_message',
        #     'schedule': crontab(hour=18, minute=5),  # 5 mins after email
        # },
        #uncomment below code when you want to test for SMS
        # 'send-sms-reminder': {
        #     'task': 'tasks.send_sms_reminder',
        #     'schedule': crontab(hour=18, minute=10),  # 10 mins after email
        # }
        'send-professional-reminders': {
            'task': 'tasks.send_reminders_for_pending_requests',
            'schedule': crontab(hour=18, minute=0),  # Runs daily at 6 PM IST
        },
        'send_monthly_activity_report': {
            'task': 'tasks.send_monthly_activity_report',
            'schedule': crontab(day_of_month=1, hour=8, minute=00),  # Runs on 1st of every month at 8 AM
        },
         'refresh-service-cache': {
        'task': 'tasks.refresh_service_cache',
        'schedule': crontab(minute="*/5"),  # Runs every 5 minutes
        }
    }


from flask_caching import Cache

cache = Cache()

def init_cache(app):
    cache.init_app(app, config={
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": app.config["CACHE_REDIS_HOST"],
        "CACHE_REDIS_PORT": app.config["CACHE_REDIS_PORT"],
        "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],
    })
