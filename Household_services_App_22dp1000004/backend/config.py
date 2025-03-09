import os
from datetime import timedelta
from flask_jwt_extended import JWTManager

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///household_services.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = "redis://localhost:6379/0"
     # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')  # Use a secure key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)  # Increase access token expiration
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7) # Increase refresh token expiration