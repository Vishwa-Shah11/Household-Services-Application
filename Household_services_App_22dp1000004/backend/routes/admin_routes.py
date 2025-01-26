from flask import Blueprint, request, jsonify

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/create_service', methods=['POST'])
def create_service():
    data = request.json
    # Logic to create a service
    return jsonify({'message': 'Service created successfully'})
