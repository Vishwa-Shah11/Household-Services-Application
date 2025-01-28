from flask import Blueprint, request, jsonify
from models import db, user, service
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from utils import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Dashboard
@admin_bp.route('/dashboard', methods=['GET'])
@role_required('Admin')
@jwt_required()
def admin_dashboard():
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403
    return jsonify({"msg": "Welcome to the admin dashboard!"}), 200


# Flag (Block) a User
@admin_bp.route('/flag_user/<int:user_id>', methods=['POST'])
@role_required('Admin')
@jwt_required()
def flag_user(user_id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403

    target_user = user.query.get_or_404(user_id)
    target_user.tokens_revoked = True  # Revoke the user's tokens
    target_user.is_blocked = True  # Block the user
    db.session.commit()
    return jsonify({"msg": f"User {target_user.username} has been flagged and tokens revoked."}), 200


# Approve a Professional
@admin_bp.route('/approve_user/<int:user_id>', methods=['PUT'])
@role_required('Admin')
@jwt_required()
def approve_user(user_id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403

    target_user = user.query.get_or_404(user_id)
    if target_user.role != 'professional':
        return jsonify({"error": "Only professionals can be approved"}), 400

    target_user.is_approved = True
    db.session.commit()
    return jsonify({"msg": f"User {target_user.username} has been approved."}), 200


# Create a New Service
@admin_bp.route('/create_service', methods=['POST'])
@role_required('Admin')
@jwt_required()
def create_service():
    data = request.json
    if not all(key in data for key in ('name', 'base_price', 'description')):
        return jsonify({"error": "Missing required fields"}), 400

    new_service = service(
        name=data['name'],
        base_price=data['base_price'],
        description=data['description']
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'message': 'Service created successfully'}), 201


# Update an Existing Service
@admin_bp.route('/update_service/<int:service_id>', methods=['PUT'])
@role_required('Admin')
@jwt_required()
def update_service(service_id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403

    existing_service = service.query.get_or_404(service_id)
    data = request.json
    existing_service.name = data.get('name', existing_service.name)
    existing_service.base_price = data.get('base_price', existing_service.base_price)
    existing_service.description = data.get('description', existing_service.description)
    db.session.commit()

    return jsonify({"msg": "Service updated successfully"}), 200


# Delete an Existing Service
@admin_bp.route('/delete_service/<int:service_id>', methods=['DELETE'])
@role_required('Admin')
@jwt_required()
def delete_service(service_id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403

    existing_service = service.query.get_or_404(service_id)
    db.session.delete(existing_service)
    db.session.commit()
    return jsonify({"msg": "Service deleted successfully"}), 200


# Get All Users (Admin Overview)
@admin_bp.route('/users', methods=['GET'])
@role_required('Admin')
@jwt_required()
def get_all_users():
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403

    all_users = user.query.all()
    result = [
        {
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role,
            'is_approved': u.is_approved,
            'is_blocked': u.is_blocked
        }
        for u in all_users
    ]
    return jsonify(result), 200



# Admin search for professionals
@admin_bp.route('/search_professionals', methods=['GET'])
@jwt_required()
def search_professionals():
    claims = get_jwt_identity()
    if claims['role'] != 'Admin':
        return jsonify({'error': 'Admins only!'}), 403

    query_params = request.args
    filters = [user.role == 'Professional']

    if 'name' in query_params:
        filters.append(user.name.ilike(f"%{query_params['name']}%"))
    if 'email' in query_params:
        filters.append(user.email.ilike(f"%{query_params['email']}%"))

    professionals = user.query.filter(*filters).all()
    results = [{'id': p.id, 'name': p.name, 'email': p.email, 'is_approved': p.is_approved, 'is_blocked': p.is_blocked} for p in professionals]

    return jsonify({'professionals': results}), 200
