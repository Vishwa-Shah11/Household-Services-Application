from flask import Blueprint, request, jsonify
from models import db, user, service
from flask_jwt_extended import jwt_required, get_jwt
from utils import role_required


admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/admin/dashboard', methods=['GET'])
@role_required('Admin')
@jwt_required()
def admin_dashboard():
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403
    return jsonify({"msg": "Welcome to the admin dashboard!"}), 200


@admin_bp.route('/flag_user/<int:user_id>', methods=['POST'])
@role_required('Admin')
@jwt_required()
def flag_user(user_id):
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403

    user = user.query.get_or_404(user_id)
    user.tokens_revoked = True  # Revoke the user's tokens
    db.session.commit()
    return jsonify({"msg": f"User {user.username} has been flagged and tokens revoked."}), 200


@admin_bp.route('/create_service', methods=['POST'])
@role_required('Admin')
def create_service():
    data = request.json
    # Logic to create a service
    new_service = service(name=data['name'], base_price=data['base_price'], description=data['description'])
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'message': 'Service created successfully'}), 201
