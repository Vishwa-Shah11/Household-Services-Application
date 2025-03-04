from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import jwt
from flask import current_app as app
from models import db, User
from flask_cors import cross_origin, CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth_bp)

@auth_bp.route('/register', methods=['POST'])
@cross_origin()
def register():
    try :
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')  # 'Admin', 'Professional', or 'Customer'

        # Validate input
        if not username or not email or not password or not role:
            return jsonify({'message': 'All fields are required'}), 400

        # Ensure only one Admin can be created
        if role == 'Admin' and User.query.filter_by(role='Admin').first():
            return jsonify({'message': 'An admin already exists'}), 403

        # Check if email exists
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists'}), 409
        
        hashed_password = generate_password_hash(password, method='sha256')
        
        # Create new user
        new_user = User(username=username, email=email, role=role, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': f'{role} registered successfully!'}), 201

    except Exception as e:
        print(f"Error in register function: {str(e)}")  # Log the error
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500
    

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
        if not new_user or not new_user.check_password(password):
            return jsonify({'message': 'Invalid credentials'}), 401

        # Generate JWT token
        access_token = create_access_token(identity={'id': new_user.id, 'role': new_user.role})
        return jsonify({'message': 'Login successful', 'token': access_token, 'role': new_user.role}), 200
    
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
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
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