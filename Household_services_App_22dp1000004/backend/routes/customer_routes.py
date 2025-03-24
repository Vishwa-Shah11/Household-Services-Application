from flask import Blueprint, request, jsonify
from models import db, Service, ServiceRequest, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from utils import role_required, get_customer_id_from_token
from models.service import ServiceCategory
from sqlalchemy.sql import func

customer_bp = Blueprint('Customer', __name__, url_prefix='/customer')

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
    # categories = db.session.query(Service.category).distinct().all()
    categories = [category.value for category in ServiceCategory]
   
    print("Categories : ", categories)
    # print(type(categories),type(categories[0]),type(categories[0][0]))
    # print(type(str(categories[0])))
    return jsonify([str(category) for category in categories]), 200

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
    
    # Check if the professional exists and is approved
    professional = User.query.filter_by(id=data.get('professional_id'), role='Professional', is_approved=True).first()
    if not professional:
        return jsonify({'error': 'Selected professional is not available'}), 404

    new_request = ServiceRequest(
        service_id=service.id,
        customer_id=customer_id,
        professional_id=professional.id,
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
    customer_id_input = get_customer_id_from_token(token)

    if not customer_id_input:
        print("❌ Invalid or expired token")
        return jsonify({"error": "Invalid or expired token"}), 401   

    try:
        service_requests = ServiceRequest.query.filter_by(customer_id=customer_id_input).all()
        # service_requests = Service.query.filter_by(category=customer_id_input).all()
        print("service_requests : ", service_requests)
        # print(service_requests[0].id,service_requests[0].service_id,service_requests[0].customer_id,"my name is heet shah ")
        if not service_requests:
            print("ℹ️ No service requests found for customer_id:", customer_id_input)
            return jsonify({"service_requests": []}), 200  # Empty response instead of None
        
        response_data = []
        # print(response_data,"vishwa shah")
        for req in service_requests:
            # print("hello sir ",req.service_id)  

            service = Service.query.get(req.service_id)
            # print("service : ", service,"narendra modi")
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


# Close an existing service request with rating & remarks
@customer_bp.route('/fetch_requests/<int:request_id>/close', methods=['PUT'])
@role_required('Customer')
@jwt_required()
def close_service_request(request_id):
    try:
        customer_id = get_jwt_identity()['id']
        # Get rating & remarks from frontend
        data = request.get_json()
        service_rating = data.get("service_rating")
        professional_rating = data.get("professional_rating")
        remarks = data.get("remarks", "")

        if not service_rating or not (1 <= service_rating <= 5):
            return jsonify({'error': 'Invalid Service rating. Must be between 1 to 5.'}), 400
        if not professional_rating or not (1 <= professional_rating <= 5):
            return jsonify({'error': 'Invalid Professional rating. Must be between 1 to 5.'}), 400

        # Fetch service request
        service_request = ServiceRequest.query.filter_by(id=request_id, customer_id=customer_id).first()
        if not service_request:
            return jsonify({'error': 'Service request not found'}), 404
        
        # Fetch the professional user
        professional = User.query.get(service_request.professional_id)
        if not professional:
            return jsonify({"error": "Assigned professional not found"}), 404
        
        # update service details
        service_request.service_status = 'Closed'
        service_request.date_of_completion = datetime.utcnow()
        service_request.remarks = remarks  # Store remarks
        service_request.rating = service_rating  # Store rating (Ensure the model has this column)

        # Update professional rating (average of all ratings received)
        if professional.rating is None:
            professional.rating = professional_rating
        else:
            existing_requests = ServiceRequest.query.filter_by(professional_id=professional.id).count()
            professional.rating = ((professional.rating * (existing_requests - 1)) + professional_rating) / existing_requests

        db.session.commit()
        return jsonify({'message': 'Service request closed successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get professionals for a specific category
@customer_bp.route('/professionals/<int:service_id>', methods=['GET'])
@role_required('Customer')
@jwt_required()
def get_professionals_for_service(service_id):
    # Ensure the service exists
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    # print(f"Service Category: {service.category}")
    professionals = (
        db.session.query(User, func.count(ServiceRequest.id).label("review_count"))
        .join(ServiceRequest, ServiceRequest.professional_id == User.id, isouter=True)
        .filter(
            User.role == "Professional",
            User.is_approved == True,
            User.category == service.category,
            # ServiceRequest.service_id == service_id
        )
        .group_by(User.id)
        .order_by(User.rating.desc(), func.count(ServiceRequest.id).desc())
        .all()
    )
    # print(f"Professionals found: {professionals}")
    if not professionals:
        return jsonify({'error': 'No professionals available for this service'}), 404
    # Return professionals as a list
    professional_list = [
        {
            "id": prof.id,
            "username": prof.username,
            "rating": getattr(prof, "rating", 0),
            "review_count": review_count,
            "base_price": service.base_price
        }
        for prof, review_count  in professionals
    ]
    return jsonify(professional_list), 200

@customer_bp.route('/select-professional/<int:service_id>', methods=['POST'])
@role_required('Customer')
@jwt_required()
def select_professional(service_id):
    data = request.json
    print("Select Professional Data:", data)

    customer_id = get_jwt_identity()['id']

    # Fetch the service and its category
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    service_category = service.category  # Get the category of the selected service

    # Check if the professional exists and is approved
    professional = User.query.filter_by(
        id=data.get('professional_id'), 
        role='Professional', 
        is_approved=True,
        category=service_category
    ).first()
    
    if not professional:
        return jsonify({'error': 'No professionals available for this category'}), 404
    
    user = User.query.get_or_404(customer_id)

    # ✅ Create a new service request (instead of using request_id)
    new_service_request = ServiceRequest(
        service_id=service_id,
        customer_id=customer_id,
        professional_id=professional.id,
        date_of_request=datetime.utcnow(),
        service_status='Assigned',
        remarks=data.get('remarks', '${user.username} requested this service')
    )
    db.session.add(new_service_request)
    db.session.commit()

    # return jsonify({'message': 'Professional selected successfully'}), 200
    return jsonify({'message': 'Service Request created successfully'})

@customer_bp.route("/summary", methods=["GET"])
@jwt_required()
def customer_summary():
    user_identity = get_jwt_identity()  # Get logged-in customer's ID

    if isinstance(user_identity, dict):  # If user_identity is a dict, extract the ID
        user_id = user_identity.get("id")
    else:
        user_id = user_identity  # Otherwise, assume it's already an integer

    if not user_id:
        return jsonify({"error": "Invalid user identity"}), 400

    # Fetch counts for requested, assigned, and closed service requests
    requested_count = ServiceRequest.query.filter_by(customer_id=user_id, service_status="Requested").count()
    assigned_count = ServiceRequest.query.filter_by(customer_id=user_id, service_status="Assigned").count()
    closed_count = ServiceRequest.query.filter_by(customer_id=user_id, service_status="Closed").count()

    return jsonify({
        "Requested": requested_count,
        "Assigned": assigned_count,
        "Closed": closed_count
    })
