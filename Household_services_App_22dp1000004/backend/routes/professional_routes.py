from flask import Blueprint, request, jsonify
from models import db, User, ServiceRequest
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from utils import role_required
from sqlalchemy.exc import SQLAlchemyError
import os
from werkzeug.utils import secure_filename # Securely save files to disk
# from flask import current_app as app
from flask import send_from_directory

professional_bp = Blueprint('professional', __name__, url_prefix='/professional')

UPLOAD_FOLDER = "uploads/"  # Define where files will be stored
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "jpg", "png"}  # Allowed formats

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Function to check file extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@professional_bp.route("/uploads/<filename>")
def serve_uploaded_file(filename):
    return send_from_directory("uploads", filename)

# Route for professionals to upload profile documents
@professional_bp.route("/upload_docs", methods=["POST"])
@role_required("Professional")
@jwt_required()
def upload_profile_docs():
    user_id = get_jwt_identity()['id']  # Get the logged-in user ID
    # print(f"Received user_id: {user_id}")
    if not user_id:
        return jsonify({"error": "User ID not found in JWT"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # print(request.files)

    if "profile_docs" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["profile_docs"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Validate file extension
    if file.filename.split('.')[-1].lower() not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Invalid file type"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        # file_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{user.username}_{filename}")
        file.save(file_path)

        # Update database with file path
        user.profile_docs = file_path
        db.session.commit()

        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200

    return jsonify({"error": "Invalid file type"}), 400

@professional_bp.route('/dashboard', methods=['GET'])
@role_required('Professional')
@jwt_required()
def professional_dashboard():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Welcome to Professional Dashboard, {current_user["id"]}'}), 200


# 1. View all service requests
@professional_bp.route('/service_requests', methods=['GET'])
@role_required('Professional')
@jwt_required()
def view_all_service_requests():
    professional_id = get_jwt_identity()['id']
     # Fetch the professional's details
    professional = User.query.filter_by(id=professional_id, role="Professional").first()
    # Check if the professional is approved
    if not professional or not professional.is_approved:
        return jsonify({'message': 'Access denied. Your account is not approved yet.'}), 403
    # Fetch all service requests that are either assigned to the professional or still open
    service_requests = ServiceRequest.query.filter(
        (ServiceRequest.professional_id == professional_id) | 
        (ServiceRequest.professional_id == None)  # Show unassigned requests too
    ).all()
    # service_requests = ServiceRequest.query.filter_by(professional_id=professional_id).all()

    if not service_requests:
        return jsonify({'message': 'No service requests available'}), 404
    
    results = [{
            'id': req.id,
            'service_id': req.service_id,
            'customer_id': req.customer_id,
            'date_of_request': req.date_of_request.strftime('%d-%m-%Y %I:%M %p'),
            # 'date_of_completion': req.date_of_completion.strftime('%d-%m-%Y %I:%M %p'),
            'service_status': req.service_status,
            'remarks': req.remarks
        } for req in service_requests
    ]

    return jsonify({'service_requests': results}), 200


# 2. Accept or reject a service request
@professional_bp.route('/service_requests/<int:request_id>/action', methods=['PUT'])
@role_required('Professional')
@jwt_required()
def action_on_service_request(request_id):
    data = request.json
    professional_id = get_jwt_identity()['id']
    service_request = ServiceRequest.query.filter_by(id=request_id, professional_id=None).first()
    if not service_request:
        return jsonify({'error': 'Service request not found or already assigned'}), 404

    if service_request.professional_id and service_request.professional_id != professional_id:
        return jsonify({'error': 'You are not assigned to this service request'}), 403
    
    if data.get('action') not in ['Accepted', 'Rejected']:
        return jsonify({'error': 'Please "Accept" or "Reject" this Service.'}), 400

    if data.get('action') == 'Accepted':
        service_request.professional_id = professional_id
        service_request.service_status = 'Assigned'
    elif data.get('action') == 'Rejected':
        service_request.professional_id = None
        service_request.service_status = 'Rejected'
    try :
        db.session.commit()
        return jsonify({'message': f'Service request {data["action"]} successfully'}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error while updating status'}), 500

# 3. Close a service request once completed
@professional_bp.route('/service_requests/<int:request_id>/close', methods=['PUT'])
@role_required('Professional')
@jwt_required()
def close_service_request(request_id):
    professional_id = get_jwt_identity()['id']
    service_request = ServiceRequest.query.filter_by(id=request_id, professional_id=professional_id, service_status='Assigned').first()
    if not service_request:
        return jsonify({'error': 'Service request not found or already closed'}), 404

    service_request.service_status = 'Closed'
    service_request.date_of_completion = datetime.utcnow()

    try :
        db.session.commit()
        return jsonify({'message': 'Service request closed successfully'}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Database error while closing service request'}), 500
    
from sqlalchemy.sql import func
@professional_bp.route('/summary', methods=['GET'])
@role_required('Professional')
@jwt_required()
def get_professional_summary():
    jwt_identity = get_jwt_identity()
    professional_id = jwt_identity.get("id")
    # print(f"Extracted professional_id: {professional_id}, Type: {type(professional_id)}")

    if not professional_id:
        return jsonify({"error": "Invalid professional ID"}), 400

    try:
        # Fetch professional's rating
        professional = User.query.get(int(professional_id))
        if not professional or professional.role != 'Professional':
            return jsonify({"error": "Unauthorized"}), 403

        rating = professional.rating

        # Fetch service request summary
        requested = ServiceRequest.query.filter_by(professional_id=professional_id, service_status="Requested").count()
        assigned = ServiceRequest.query.filter_by(professional_id=professional_id, service_status="Assigned").count()
        closed = ServiceRequest.query.filter_by(professional_id=professional_id, service_status="Closed").count()
        rejected = ServiceRequest.query.filter_by(professional_id=professional_id, service_status="Rejected").count()

        return jsonify({
            "Rating": rating,
            "Requested": requested,
            "Assigned": assigned,
            "Closed": closed,
            "Rejected": rejected
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500