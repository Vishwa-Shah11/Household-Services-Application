from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)  # Admin/Customer/Professional
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10))
    address = db.Column(db.Text)
    phone = db.Column(db.String(15))
    profile_docs = db.Column(db.String(255))  # For professionals only
    experience = db.Column(db.String(255))  # For professionals only
    rating = db.Column(db.Integer)  # For professionals only
    is_approved = db.Column(db.Boolean, default=False)  # For professionals
    is_blocked = db.Column(db.Boolean, default=False)  # To block a user

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

    def set_password(self, password):
        """Hash and set password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hashed value."""
        return check_password_hash(self.password, password)