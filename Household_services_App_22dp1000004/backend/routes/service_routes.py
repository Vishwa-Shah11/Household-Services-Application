from flask import Blueprint, jsonify, request
from models import Service
from utils import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity

service_bp = Blueprint('service_bp', __name__)

# Search for available services
@service_bp.route('/search', methods=['GET'])
@role_required('Customer')
@jwt_required()
def search_services():
    current_user = get_jwt_identity()  # Get user from token
    # print(f"User {current_user} is searching...")  # Debugging

    query = request.args.get('query', '').strip().lower()
    # print("Query:", query)
    if not query:
        return jsonify({'services': []}), 200  # Return empty if query is empty
    
    # Search by name or category
    services = Service.query.filter(
        (Service.name.ilike(f"%{query}%")) | (Service.category.ilike(f"%{query}%"))
    ).all()

    # print("Services", services)

    # Serialize results
    service_list = [{'id': s.id, 'name': s.name, 'category': s.category} for s in services]
    # print("Service list", service_list)
    return jsonify({'services': service_list})


@service_bp.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'error': 'Service not found'}), 404

    return jsonify({
        'id': service.id,
        'name': service.name,
        'category': service.category,
        'description': service.description,
        'base_price': service.base_price,
        'time_required': service.time_required,
    })
