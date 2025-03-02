from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Import models here
from .user import User
from .service import Service
from .service_request import ServiceRequest