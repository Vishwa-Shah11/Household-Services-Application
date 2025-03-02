from flask import Blueprint, request, jsonify
from models import db, Service, ServiceRequest
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from utils import role_required

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/dashboard', methods=['GET'])
@role_required('Customer')
@jwt_required()
def customer_dashboard():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Welcome to Customer Dashboard, {current_user["id"]}'}), 200

@customer_bp.route('/services', methods=['GET'])
@jwt_required()
def get_available_services():
    services = Service.query.all()
    print(Service.query.all())
    service_list = [{
        "id": s.id,
        "name": s.name,
        "base_price": s.base_price,
        "description": s.description,
        'time_required': s.time_required
    } for s in services]

    print("Fetched Services:", service_list)
    return jsonify({"services": service_list}), 200

#Create a new service request
@customer_bp.route('/service_request', methods=['POST'])
@role_required('Customer')
@jwt_required()
def create_service_request():
    data = request.json
    customer_id = get_jwt_identity()['id']

    # Check if the service exists
    service = Service.query.get(data.get('service_id'))
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    new_request = ServiceRequest(
        service_id=service.id,
        customer_id=customer_id,
        date_of_request=datetime.utcnow(),
        service_status='requested',
        remarks=data.get('remarks', '')  # Default empty remarks if not provided
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Service request created successfully', 'request_id': new_request.id}), 201


# 2. Edit an existing service request
@customer_bp.route('/service_request/<int:request_id>', methods=['PUT'])
@role_required('Customer')
@jwt_required()
def edit_service_request(request_id):
    data = request.json
    customer_id = get_jwt_identity()['id']

    service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=customer_id).first()
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    # Update fields if provided
    if 'date_of_request' in data:
        try :
            service_request.date_of_request = datetime.strptime(data['date_of_request'], '%Y-%m-%d %H:%M:%S')
        except ValueError :
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400
    if 'service_status' in data:
        if data['service_status'] not in ['requested', 'assigned', 'closed']:
            return jsonify({'error': 'Invalid service status'}), 400
        service_request.service_status = data['service_status']
    if 'remarks' in data:
        service_request.remarks = data['remarks']

    db.session.commit()
    return jsonify({'message': 'Service request updated successfully'}), 200


# 3. Close an existing service request
@customer_bp.route('/service_request/<int:request_id>/close', methods=['PUT'])
@role_required('Customer')
@jwt_required()
def close_service_request(request_id):
    customer_id = get_jwt_identity()['id']

    service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=customer_id).first()
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    service_request.service_status = 'closed'
    service_request.date_of_completion = datetime.utcnow()

    db.session.commit()
    return jsonify({'message': 'Service request closed successfully'}), 200


# 4. Search for available services
@customer_bp.route('/search_services', methods=['GET'])
@role_required('Customer')
@jwt_required()
def search_services():
    query_params = request.args
    filters = []

    if 'name' in query_params:
        filters.append(Service.name.ilike(f"%{query_params['name']}%"))
    if 'location' in query_params:  # Assuming a location field exists in the service model
        filters.append(Service.location.ilike(f"%{query_params['location']}%"))
    if 'pin_code' in query_params:  # Assuming a pin_code field exists in the service model
        filters.append(Service.pin_code == query_params['pin_code'])

    services = Service.query.filter(*filters).all()
    results = [{'id': s.id, 'name': s.name, 'description': s.description, 'base_price': s.base_price} for s in services]

    return jsonify({'services': results}), 200
