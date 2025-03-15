from . import db
from enum import Enum

class ServiceCategory(Enum):
    SALOON_AND_SPA = "Saloon & Spa"
    PLUMBING = "Plumbing"
    ELECTRICIAN = "Electrician"
    CLEANING = "Cleaning"
    CARPENTRY = "Carpentry"
    PAINTING = "Painting"
    APPLIANCE_REPAIR = "Appliance Repair"
    PEST_CONTROL = "Pest Control"
    # OTHERS = "Others"

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # category = db.Column(db.Enum(ServiceCategory), nullable=False)
    # category = db.Column(Enum(ServiceCategory, values_callable=lambda x: [e.value for e in x]), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    time_required = db.Column(db.Integer, nullable=False)  # In minutes

    def __repr__(self):
        return f"<Service {self.name}>"