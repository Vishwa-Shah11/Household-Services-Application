from flask import Blueprint, request, jsonify
from utils import role_required

professional_bp = Blueprint('professional', __name__, url_prefix='/api/professional')

@professional_bp.route('/accept_request/<int:request_id>', methods=['PUT'])
@role_required('Professional')
def accept_request(request_id):
    data = request.json
    # Logic to accept a service request
    return jsonify({'message': 'Request accepted successfully'}), 200
