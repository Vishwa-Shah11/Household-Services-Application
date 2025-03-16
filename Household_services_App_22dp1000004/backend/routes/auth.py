from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app as app
from models import db, User, Service
from flask_cors import cross_origin, CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from models.service import ServiceCategory

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth_bp)

UPLOAD_FOLDER = "uploads"  # Directory to save uploaded files
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "doc", "docx"}  # Allowed file types

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# @auth_bp.route('/register', methods=['POST'])
# @cross_origin()
# def register():
#     try :
#         data = request.json
#         # common fields
#         role = data.get('role')  # 'Professional', or 'Customer'
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         pincode = data.get('pincode')
#         address = data.get('address')
#         phone = data.get('phone')

#         # Validate input
#         if not username or not email or not password or not role:
#             return jsonify({'message': 'All fields are required'}), 400

#         # Ensure only one Admin can be created
#         if role == 'Admin' and User.query.filter_by(role='Admin').first():
#             return jsonify({'message': 'An admin already exists'}), 403

#         # Check if email exists
#         if User.query.filter_by(email=email).first():
#             return jsonify({'message': 'Email already registered'}), 409
        
#         hashed_password = generate_password_hash(password, method='sha256')
        
#         # Create new user
#         # new_user = User(username=username, email=email, role=role, password=hashed_password)
#         # Create user based on role
#         if role == "Customer":
#             new_user = User(
#                 role=role,
#                 username=username,
#                 email=email,
#                 password=hashed_password,
#                 pincode=pincode,
#                 address=address,
#                 phone=phone
#             )
#         elif role == "Professional":
#             profile_docs = data.get('profile_docs')  # Professional-specific field
#             experience = data.get('experience')  # Professional-specific field
#             rating = data.get('rating', 0)  # Default rating = 0
#             new_user = User(
#                 role=role,
#                 username=username,
#                 email=email,
#                 password=hashed_password,
#                 pincode=pincode,
#                 address=address,
#                 phone=phone,
#                 profile_docs=profile_docs,
#                 experience=experience,
#                 rating=rating,
#                 is_approved=False  # Professionals need approval
#             )
#             db.session.add(new_user)
#             db.session.commit()

#             return jsonify({'message': f'{role} registered successfully!'}), 201

#     except Exception as e:
#         print(f"Error in register function: {str(e)}")  # Log the error
#         return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500

@auth_bp.route("/get_categories", methods=["GET"])
def get_categories():
    # categories = db.session.query(Service.category).distinct().all()
    # categories_list = [category[0].value for category in categories] 
    categories_list = [category.value for category in ServiceCategory]
    # print(categories_list,"hi vishwa shah ")
    return jsonify({"categories": categories_list}), 200

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        print("🚀 Received Register Request!")
        file_path = None
        # service_category = Service.query.filter_by(category=category).all()
        # print("🔍 Service Category:", service_category)

        # Check content type
        if request.content_type == "application/json":
            data = request.get_json()
            print("🔍 JSON Data:", data)
            role = data.get("role")
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            pincode = data.get("pincode")
            address = data.get("address")
            phone = data.get("phone")
            experience = data.get("experience")
            category = data.get("category")
            profile_docs = None  # No file upload in JSON requests

        elif request.content_type.startswith("multipart/form-data"):
            print("🔍 Handling Form-Data Request")
            role = request.form.get("role")
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            pincode = request.form.get("pincode")
            address = request.form.get("address")
            phone = request.form.get("phone")
            experience = request.form.get("experience")
            category = request.form.get("category")
            profile_docs = request.files.get("profile_docs")  # Get file

            # Handle file upload
            
            if role == "Professional" and profile_docs and allowed_file(profile_docs.filename):
                filename = secure_filename(profile_docs.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                profile_docs.save(file_path)
                print(f"✅ File uploaded: {file_path}")
        else:
            return jsonify({"error": "Unsupported Content-Type"}), 400

        # Ensure required fields exist
        if not role or not username or not email or not password:
            # print("❌ Missing Required Fields")
            return jsonify({"error": "Missing required fields"}), 400
        
        if role == "Professional":
            # catogaries=Service.query.all()
            if not category:
                return jsonify({"error": "Professionals must select a category"}), 400
            # # Ensure category is valid
            # if category not in [c.value for c in Service.ServiceCategory]:
            #     return jsonify({"error": "Invalid category"}), 400
    
        hashed_password = generate_password_hash(password, method='sha256')

        # Debug output
        print("📝 User Data:", {
            "role": role,
            "username": username,
            "email": email,
            "pincode": pincode,
            "address": address,
            "phone": phone,
            "category": category if role == "Professional" else None,
            "experience": experience if role == "Professional" else None,
            "profile_docs": file_path if role == "Professional" else None,
        })

        # 🚀 Save user to database (Modify this based on your DB model)
        new_user = User(
            role=role,
            username=username,
            email=email,
            password=hashed_password,  # Hash before saving!
            pincode=pincode,
            address=address,
            phone=phone,
            category=category if role == "Professional" else None,
            experience=experience if role == "Professional" else None,
            profile_docs=file_path if role == "Professional" else None,
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': f'{role} registered successfully!',
            "user": {
                "role": role,
                "username": username,
                "email": email,
                "pincode": pincode,
                "address": address,
                "phone": phone,
                "experience": experience if role == "Professional" else None,
                "profile_docs": file_path if role == "Professional" else None,
            }
        }), 201

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    try :
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email:
            return jsonify({'message': 'Please enter your Email'}), 400
        
        if not password:
            return jsonify({'message': 'Please enter your Password'}), 400

        # Find user by email
        new_user = User.query.filter_by(email=email).first()
        print(new_user)
        print(check_password_hash(new_user.password, password))
        if not new_user or not check_password_hash(new_user.password, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if user is blocked
        if new_user.is_blocked:
            return jsonify({'error': 'Your account is blocked. Please contact support.'}), 403  # Forbidden

        # Generate JWT token
        access_token = create_access_token(identity={'id': new_user.id, 'role': new_user.role, 'username': new_user.username})
        return jsonify({
            'message': 'Login successful', 
            'token': access_token, 
            'role': new_user.role, 
            'username': new_user.username
        }), 200
    
    except Exception as e:
        print(f"Error in login function: {str(e)}")  # Logs error for debugging
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@cross_origin()
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully!'}), 200


@auth_bp.route('/load_user', methods=['GET'])
@cross_origin()
def load_user():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing'}), 403

    try:
        data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'user': {'id': user.id, 'email': user.email, 'role': user.role}}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()  # Get user details from JWT
    user_id = current_user['id']  # Extract only the ID
    user = User.query.filter_by(id=user_id).first()  # Query with the extracted ID
    
    # print("usr:", user)
    
    if user:
        print("name:", user.username)
        return jsonify({'name': user.username})
    
    return jsonify({'error': 'User not found'}), 404