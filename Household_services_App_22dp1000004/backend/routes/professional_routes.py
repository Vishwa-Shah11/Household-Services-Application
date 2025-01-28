from flask import Blueprint, request, jsonify
from models import db, service_request, user
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

professional_bp = Blueprint('professional', __name__, url_prefix='/professional')

# 1. View all service requests
@professional_bp.route('/service_requests', methods=['GET'])
@jwt_required()
def view_all_service_requests():
    professional_id = get_jwt_identity()['id']

    # Check if the user is a professional
    professional = user.query.filter_by(id=professional_id, role='Professional').first()
    if not professional:
        return jsonify({'error': 'Only professionals can access this endpoint'}), 403

    service_requests = service_request.query.filter_by(professional_id=professional_id).all()
    results = [
        {
            'id': req.id,
            'service_id': req.service_id,
            'customer_id': req.customer_id,
            'date_of_request': req.date_of_request,
            'date_of_completion': req.date_of_completion,
            'service_status': req.service_status,
            'remarks': req.remarks
        } for req in service_requests
    ]

    return jsonify({'service_requests': results}), 200


# 2. Accept or reject a service request
@professional_bp.route('/service_request/<int:request_id>/action', methods=['PUT'])
@jwt_required()
def action_on_service_request(request_id):
    data = request.json
    professional_id = get_jwt_identity()['id']

    # Check if the user is a professional
    professional = user.query.filter_by(id=professional_id, role='Professional').first()
    if not professional:
        return jsonify({'error': 'Only professionals can access this endpoint'}), 403

    serviceRequest = service_request.query.filter_by(id=request_id).first()
    if not serviceRequest:
        return jsonify({'error': 'Service request not found'}), 404

    if serviceRequest.professional_id and serviceRequest.professional_id != professional_id:
        return jsonify({'error': 'You are not assigned to this service request'}), 403

    if data.get('action') == 'accept':
        serviceRequest.professional_id = professional_id
        serviceRequest.service_status = 'assigned'
        db.session.commit()
        return jsonify({'message': 'Service request accepted'}), 200

    elif data.get('action') == 'reject':
        serviceRequest.professional_id = None
        serviceRequest.service_status = 'rejected'
        db.session.commit()
        return jsonify({'message': 'Service request rejected'}), 200

    else:
        return jsonify({'error': 'Invalid action. Use "accept" or "reject"'}), 400


# 3. Close a service request once completed
@professional_bp.route('/service_request/<int:request_id>/close', methods=['PUT'])
@jwt_required()
def close_service_request(request_id):
    professional_id = get_jwt_identity()['id']

    # Check if the user is a professional
    professional = user.query.filter_by(id=professional_id, role='Professional').first()
    if not professional:
        return jsonify({'error': 'Only professionals can access this endpoint'}), 403

    serviceRequest = service_request.query.filter_by(id=request_id, professional_id=professional_id).first()
    if not serviceRequest:
        return jsonify({'error': 'Service request not found or not assigned to you'}), 404

    if serviceRequest.service_status != 'assigned':
        return jsonify({'error': 'Service request is not in an assignable state'}), 400

    serviceRequest.service_status = 'closed'
    serviceRequest.date_of_completion = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Service request closed successfully'}), 200
