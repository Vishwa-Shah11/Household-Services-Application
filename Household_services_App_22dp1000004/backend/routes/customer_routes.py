from flask import Blueprint, request, jsonify

customer_bp = Blueprint('customer', __name__, url_prefix='/api/customer')

@customer_bp.route('/register', methods=['POST'])
def register_customer():
    data = request.json
    # Logic to register a customer
    return jsonify({'message': 'Customer registered successfully'})
