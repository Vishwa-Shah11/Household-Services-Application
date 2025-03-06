from . import db

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    time_required = db.Column(db.Integer, nullable=False)  # In minutes

    def __repr__(self):
        return f"<Service {self.name}>"
