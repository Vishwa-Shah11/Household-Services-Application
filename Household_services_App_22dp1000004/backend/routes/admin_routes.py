from flask import Blueprint, request, jsonify
from models import db, User, Service
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from utils import role_required
from sqlalchemy.sql import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Dashboard
@admin_bp.route('/dashboard', methods=['GET'])
@role_required('Admin')
@jwt_required()
def admin_dashboard():
    return jsonify({"msg": "Welcome to the admin dashboard!"}), 200

# Create a New Service
@admin_bp.route('/create_service', methods=['POST'])
@role_required('Admin')
@jwt_required()
def create_service():
    data = request.json
    print("Service Data:", data)
    required_fields = ('name', 'category', 'base_price', 'description', 'time_required');

    if not all(key in data for key in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try :
        new_service = Service(
            name=data['name'],
            category=data['category'],
            base_price=data['base_price'],
            description=data['description'],
            time_required=data.get('time_required', 0) 
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify({'message': 'Service created successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Update an Existing Service
@admin_bp.route('/update_service/<int:service_id>', methods=['PUT'])
@role_required('Admin')
@jwt_required()
def update_service(service_id):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400
    
    existing_service = Service.query.get_or_404(service_id)
    # if not existing_service:
    #     return jsonify({"error": "Service not found"}), 404
    
    existing_service.name = data.get('name', existing_service.name)
    existing_service.category = data.get('category', existing_service.category)
    existing_service.base_price = data.get('base_price', existing_service.base_price)
    existing_service.description = data.get('description', existing_service.description)
    existing_service.time_required = data.get('time_required', existing_service.time_required)

    try :
        db.session.commit()
        return jsonify({"message": "Service updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update service: {str(e)}"}), 500

#get all service list
@admin_bp.route('/services', methods=['GET'])
@role_required('Admin')
@jwt_required()
def get_services():
    services = Service.query.all()
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


# Delete an Existing Service
@admin_bp.route('/delete_service/<int:service_id>', methods=['DELETE'])
@role_required('Admin')
@jwt_required()
def delete_service(service_id):
    existing_service = Service.query.get_or_404(service_id)
    db.session.delete(existing_service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully"}), 200


# Get All Users (Admin Overview)
@admin_bp.route('/users', methods=['GET'])
@role_required('Admin')
@jwt_required()
def get_all_users():
    users = User.query.filter(User.role.in_(["Customer", "Professional"])).all()
    # print("Users:", users)
    
    users_list = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "profile_docs": user.profile_docs if user.profile_docs else "Not Uploaded",
            "is_approved": user.is_approved if user.role == "Professional" else None,  # Show only for Professionals
            "is_blocked": user.is_blocked
        } 
        for user in users
    ]
    # print("Users List:", users_list)
    return jsonify({"users": users_list}), 200


# Approve a Professional
@admin_bp.route('/approve/<int:user_id>', methods=['POST'])
@role_required('Admin')
@jwt_required()
def approve_user(user_id):
    # print(f"Approval request received for user ID: {user_id}")
    target_user = User.query.get_or_404(user_id)
    # print("Target User:", target_user)
    if target_user and target_user.role == "Professional":
        # print(f"Approving user: {target_user.username}")
        target_user.is_approved = True
        db.session.commit()
        # print(f"User {target_user.username} has been approved.")
        return jsonify({"message": f"User {target_user.username} has been approved.", "username": target_user.username}), 200
    # print("Approval not applicable.")
    return jsonify({"error": "Approval not applicable"}), 404

@admin_bp.route("/reject/<int:user_id>", methods=["POST"])
@role_required("Admin")
@jwt_required()
def reject_user(user_id):
    target_user = User.query.get_or_404(user_id)
    if target_user and target_user.role == "Professional":
        target_user.is_approved = False
        db.session.commit()
        return jsonify({"message": f"User {target_user.username} has been rejected.", "username": target_user.username}), 200
    return jsonify({"error": "Rejection not applicable"}), 404

# Admin search for professionals
@admin_bp.route('/search_professionals', methods=['GET'])
@role_required('Admin')
@jwt_required()
def search_professionals():
    try:
        current_user = get_jwt_identity()
        # Get search query parameters
        query = request.args.get('q', '').strip().lower()

        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Search professionals in DB
        professionals = User.query.filter(
            User.role == 'Professional',
            (User.username.ilike(f"%{query}%")) |  # Search by name
            (User.email.ilike(f"%{query}%"))  |  # Search by email
            (User.rating.ilike(f"%{query}%"))    # Search by rating
        ).all()

        results = [{
            'id': p.id,
            'name': p.username,
            'email': p.email,
            'rating': p.rating,
            # 'is_approved': p.is_approved,
            'is_blocked': p.is_blocked
            } for p in professionals]
        return jsonify({'professionals': results}), 200
    
    except Exception as e:
        print(f"Error in search_professionals function: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


# Flag (Block) a User
@admin_bp.route('/flag_user/<int:user_id>', methods=['POST'])
@role_required('Admin')
@jwt_required()
def flag_user(user_id):
    target_user = User.query.get_or_404(user_id)
    if target_user.role.lower() in ['professional', 'customer']:  
        avg_rating = target_user.rating  # Directly using the rating column

    if avg_rating is not None and avg_rating < 1:  # Automatic blocking for poor-rated users
        target_user.is_blocked = True
        db.session.commit()
        return jsonify({"msg": f"User {target_user.name} has been automatically blocked due to poor ratings."}), 200

    # Toggle block/unblock status
    target_user.is_blocked = not target_user.is_blocked
    db.session.commit()
    # target_user.tokens_revoked = True  # Revoke the user's tokens
    status = "blocked" if target_user.is_blocked else "unblocked"
    return jsonify({"message": f"User {target_user.username} has been {status} by Admin."}), 200
