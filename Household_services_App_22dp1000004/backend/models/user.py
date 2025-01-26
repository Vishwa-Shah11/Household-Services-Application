from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)  # Admin/Customer/Professional
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_docs = db.Column(db.String(255))  # For professionals only

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"
