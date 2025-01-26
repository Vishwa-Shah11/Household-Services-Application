from flask import Blueprint, request, jsonify

professional_bp = Blueprint('professional', __name__, url_prefix='/api/professional')

@professional_bp.route('/accept_request', methods=['POST'])
def accept_request():
    data = request.json
    # Logic to accept a service request
    return jsonify({'message': 'Request accepted successfully'})
