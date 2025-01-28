from flask import Blueprint, request, jsonify
from utils import role_required

customer_bp = Blueprint('customer', __name__, url_prefix='/api/customer')

@customer_bp.route('/register', methods=['POST'])
@role_required('Customer')
def register_customer():
    data = request.json
    # Logic to register a customer
    return jsonify({'message': 'Customer registered successfully'}), 201


@customer_bp.route('/create_request', methods=['POST'])
@role_required('Customer')
def create_request():
    # Logic to create a new service request
    return jsonify({'message': 'Request created successfully'}), 201