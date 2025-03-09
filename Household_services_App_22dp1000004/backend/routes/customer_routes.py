from flask import Blueprint, request, jsonify
from models import db, Service, ServiceRequest
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from utils import role_required, get_customer_id_from_token

customer_bp = Blueprint('Customer', __name__, url_prefix='/customer')
# print(customer_bp)

@customer_bp.route('/dashboard', methods=['GET'])
@role_required('Customer')
@jwt_required()
def customer_dashboard():
    print("🚀 REQUEST RECEIVED at /customer/dashboard")  # Debugging
    try:
        current_user = get_jwt_identity()
        print("🟢 JWT Decoded User:", current_user)  # Check if token is decoded
        return jsonify({'message': f'Welcome to Customer Dashboard, {current_user["id"]}'}), 200
    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": "Something went wrong"}), 500

@customer_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = db.session.query(Service.category).distinct().all()
    # print("Categories : ", categories)
    # print(type(categories),type(categories[0]),type(categories[0][0]))
    # print(type(str(categories[0])))
    return jsonify([str(category[0]) for category in categories]), 200

@customer_bp.route('/services/<category>', methods=['GET'])
@jwt_required()
def get_services_by_category(category):
    services = Service.query.filter_by(category=category).all()
    return jsonify({
        "services": [{
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "base_price": service.base_price,
            "time_required": service.time_required
        } for service in services]
    }), 200

@customer_bp.route('/services', methods=['GET'])
@jwt_required()
def get_available_services():
    services = Service.query.all()
    # print(Service.query.all())
    service_list = [{
        "id": s.id,
        "name": s.name,
        "category": s.category,
        "base_price": s.base_price,
        "description": s.description,
        'time_required': s.time_required
    } for s in services]

    # print("Fetched Services:", service_list)
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
        service_status='Requested',
        remarks=data.get('remarks', '')  # Default empty remarks if not provided
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Service request created successfully'}), 201

@customer_bp.route('/fetch_requests', methods=['GET'])
def fetch_requests():
    print("🚀 REQUEST RECEIVED at /customer/fetch_requests")  # Debugging
    token = request.headers.get('Authorization')
    if not token:
        print("❌ No Authorization token provided")
        return jsonify({"error": "Unauthorized"}), 401

    token = token.replace("Bearer ", "")  # Remove "Bearer " prefix
    customer_id = get_customer_id_from_token(token)

    if not customer_id:
        print("❌ Invalid or expired token")
        return jsonify({"error": "Invalid or expired token"}), 401   

    try:
        service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
        if not service_requests:
            print("ℹ️ No service requests found for customer_id:", customer_id)
            return jsonify({"service_requests": []}), 200  # Empty response instead of None
        
        response_data = []
        for req in service_requests:
            service = Service.query.get(req.service_id)
            if not service:
                print(f"⚠️ Service not found for service_id: {req.service_id}")
                continue

            response_data.append({
                "id": req.id,
                "service_id": req.service_id,
                "service_name": service.name,
                "status": req.service_status,
                "remarks": req.remarks,
                "date_of_request": req.date_of_request.strftime('%d-%m-%Y %I:%M %p')
            })
        # print("✅ Service Requests Found:", response_data)
        return jsonify({"service_requests": response_data}), 200
    except Exception as e:
        print("❌ Error fetching service requests:", str(e))
        return jsonify({"error": str(e)}), 500


# Edit an existing service request
@customer_bp.route('/fetch_requests/<int:request_id>', methods=['PUT'])
@role_required('Customer')
@jwt_required()
def edit_service_request(request_id):
    data = request.json
    print("edit_service_request data : ", data)
    token = request.headers.get("Authorization").split(" ")[1]  # Extract token
    
    customer_id = get_customer_id_from_token(token)  # Get customer ID from token
    print("customer_id : ", customer_id)

    if not customer_id:
        return jsonify({'error': 'Unauthorized'}), 401

    service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=customer_id).first()
    print(service_request)
    print(type(service_request))
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    # Update fields if provided
    if 'date_of_request' in data:
        try:
            # Parse the incoming date from format "10-03-2025 02:15 PM"
            # service_request.date_of_request = datetime.strptime(data['date_of_request'], '%d-%m-%Y %I:%M %p')
            service_request.date_of_request = service_request.date_of_request.replace(tzinfo=None)
            print("hellooooooooooooooooooo", service_request.date_of_request)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use DD-MM-YYYY HH:MM AM/PM'}), 400

    if 'service_status' in data:
        if data['service_status'] not in ['Requested', 'Assigned', 'Closed']:
            return jsonify({'error': 'Invalid service status'}), 400
        service_request.service_status = data['service_status']
    if 'remarks' in data:
        service_request.remarks = data['remarks']

    db.session.commit()
    return jsonify({'message': 'Service request updated successfully'}, 200) 

# # Edit an existing service request
# @customer_bp.route('/fetch_requests/<int:request_id>', methods=['PUT'])
# @role_required('Customer')
# @jwt_required()
# def edit_service_request(request_id):
#     data = request.json
#     token = request.headers.get("Authorization").split(" ")[1]  # Extract token
#     customer_id = get_customer_id_from_token(token)  # Get customer ID from token
#     # customer_id = get_jwt_identity()['id']

#     if not customer_id:
#         return jsonify({'error': 'Unauthorized'}), 401

#     service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=customer_id).first()
#     if not service_request:
#         return jsonify({'error': 'Service request not found'}), 404

#     try :
#     # Update fields if provided
#         if 'date_of_request' in data and data['date_of_request']:
#                 service_request.date_of_request = datetime.strptime(data['date_of_request'], '%Y-%m-%d %H:%M:%S')
#         if 'service_status' in data:
#             if data['service_status'] not in ['requested', 'assigned', 'closed']:
#                 return jsonify({'error': 'Invalid service status'}), 400
#             service_request.service_status = data['service_status']
#         if 'remarks' in data:
#             service_request.remarks = data['remarks']

#         db.session.commit()
#         return jsonify({'message': 'Service request updated successfully'}), 200
#     except ValueError :
#         return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400
#     except Exception as e:
#         return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


# Close an existing service request with rating & remarks
@customer_bp.route('/fetch_requests/<int:request_id>/close', methods=['PUT'])
@role_required('Customer')
@jwt_required()
def close_service_request(request_id):
    customer_id = get_jwt_identity()['id']
    service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=customer_id).first()

    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404

    # Get rating & remarks from frontend
    data = request.get_json()
    rating = data.get('rating', None)
    remarks = data.get('remarks', '')

    if not rating or not (1 <= rating <= 5):
        return jsonify({'error': 'Invalid rating. Must be between 1 to 5.'}), 400

    # Update service request
    service_request.service_status = 'Closed'
    service_request.date_of_completion = datetime.utcnow()
    service_request.remarks = remarks  # Store remarks
    service_request.rating = rating  # Store rating (Ensure the model has this column)

    db.session.commit()
    return jsonify({'message': 'Service request closed successfully'}), 200