from flask import Blueprint, request, jsonify
from models import db, User, ServiceRequest
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from utils import role_required
from sqlalchemy.exc import SQLAlchemyError

professional_bp = Blueprint('professional', __name__, url_prefix='/professional')

@professional_bp.route('/dashboard', methods=['GET'])
@role_required('Professional')
@jwt_required()
def professional_dashboard():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Welcome to Professional Dashboard, {current_user["id"]}'}), 200


# 1. View all service requests
@professional_bp.route('/service_requests', methods=['GET'])
@role_required('Professional')
@jwt_required()
def view_all_service_requests():
    professional_id = get_jwt_identity()['id']
    service_requests = ServiceRequest.query.filter_by(professional_id=professional_id).all()

    if not service_requests:
        return jsonify({'message': 'No service requests assigned yet'}), 404
    
    results = [{
            'id': req.id,
            'service_id': req.service_id,
            'customer_id': req.customer_id,
            'date_of_request': req.date_of_request.strftime('%d-%m-%Y %I:%M %p'),
            'date_of_completion': req.date_of_completion.strftime('%d-%m-%Y %I:%M %p'),
            'service_status': req.service_status,
            'remarks': req.remarks
        } for req in service_requests
    ]

    return jsonify({'service_requests': results}), 200


# 2. Accept or reject a service request
@professional_bp.route('/service_requests/<int:request_id>/action', methods=['PUT'])
@role_required('Professional')
@jwt_required()
def action_on_service_request(request_id):
    data = request.json
    professional_id = get_jwt_identity()['id']
    service_request = ServiceRequest.query.filter_by(id=request_id, professional_id=None).first()
    if not service_request:
        return jsonify({'error': 'Service request not found or already assigned'}), 404

    if service_request.professional_id and service_request.professional_id != professional_id:
        return jsonify({'error': 'You are not assigned to this service request'}), 403
    
    if data.get('action') not in ['Accepted', 'Rejected']:
        return jsonify({'error': 'Please "Accept" or "Reject" this Service.'}), 400

    if data.get('action') == 'Accepted':
        service_request.professional_id = professional_id
        service_request.service_status = 'Assigned'
    elif data.get('action') == 'Rejected':
        service_request.professional_id = None
        service_request.service_status = 'Rejected'
    try :
        db.session.commit()
        return jsonify({'message': f'Service request {data["action"]} successfully'}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error while updating status'}), 500

# 3. Close a service request once completed
@professional_bp.route('/service_requests/<int:request_id>/close', methods=['PUT'])
@role_required('Professional')
@jwt_required()
def close_service_request(request_id):
    professional_id = get_jwt_identity()['id']
    service_request = ServiceRequest.query.filter_by(id=request_id, professional_id=professional_id, service_status='Assigned').first()
    if not service_request:
        return jsonify({'error': 'Service request not found or already closed'}), 404

    service_request.service_status = 'Closed'
    service_request.date_of_completion = datetime.utcnow()

    try :
        db.session.commit()
        return jsonify({'message': 'Service request closed successfully'}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error while closing service request'}), 500
    