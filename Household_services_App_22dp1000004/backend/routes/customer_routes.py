from flask import Blueprint, request, jsonify
from models import db, service, service_request, user
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def customer_dashboard():
    current_user = get_jwt_identity()
    claims = get_jwt()
    if claims['role'] != 'customer':
        return jsonify({"msg": "Customer only!"}), 403
    return jsonify({'message': f'Welcome to Customer Dashboard, {current_user["id"]}'}), 200


# 1. Create a new service request
@customer_bp.route('/service_request', methods=['POST'])
@jwt_required()
def create_service_request():
    data = request.json
    customer_id = get_jwt_identity()['id']

    # Check if the service exists
    service = service.query.get(data.get('service_id'))
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    new_request = service_request(
        service_id=service.id,
        customer_id=customer_id,
        date_of_request=datetime.utcnow(),
        service_status='requested',
        remarks=data.get('remarks')
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Service request created successfully', 'request_id': new_request.id}), 201


# 2. Edit an existing service request
@customer_bp.route('/service_request/<int:request_id>', methods=['PUT'])
@jwt_required()
def edit_service_request(request_id):
    data = request.json
    customer_id = get_jwt_identity()['id']

    service_request = service_request.query.filter_by(id=request_id, customer_id=customer_id).first()
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    # Update fields
    if 'date_of_request' in data:
        service_request.date_of_request = datetime.strptime(data['date_of_request'], '%Y-%m-%d %H:%M:%S')
    if 'service_status' in data:
        service_request.service_status = data['service_status']
    if 'remarks' in data:
        service_request.remarks = data['remarks']

    db.session.commit()
    return jsonify({'message': 'Service request updated successfully'}), 200


# 3. Close an existing service request
@customer_bp.route('/service_request/<int:request_id>/close', methods=['PUT'])
@jwt_required()
def close_service_request(request_id):
    customer_id = get_jwt_identity()['id']

    service_request = service_request.query.filter_by(id=request_id, customer_id=customer_id).first()
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    service_request.service_status = 'closed'
    service_request.date_of_completion = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Service request closed successfully'}), 200


# 4. Search for available services
@customer_bp.route('/search_services', methods=['GET'])
@jwt_required()
def search_services():
    query_params = request.args
    filters = []

    if 'name' in query_params:
        filters.append(service.name.ilike(f"%{query_params['name']}%"))
    if 'location' in query_params:  # Assuming a location field exists in the service model
        filters.append(service.location.ilike(f"%{query_params['location']}%"))
    if 'pin_code' in query_params:  # Assuming a pin_code field exists in the service model
        filters.append(service.pin_code == query_params['pin_code'])

    services = service.query.filter(*filters).all()
    results = [{'id': s.id, 'name': s.name, 'description': s.description, 'base_price': s.base_price} for s in services]

    return jsonify({'services': results}), 200
