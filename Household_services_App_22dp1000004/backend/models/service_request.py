from . import db

class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime)
    service_status = db.Column(db.String(20), nullable=False)  # Requested/Assigned/Rejected/Closed
    action = db.Column(db.String(20))  # Accepted/Rejected
    remarks = db.Column(db.Text)
    # rating = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<ServiceRequest {self.id} ({self.service_status})>"
