from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app as app
from models import db, user
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
@cross_origin()
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # 'Admin', 'Professional', or 'Customer'

    # Validate input
    if not username or not password or not role:
        return jsonify({'message': 'All fields are required'}), 400

    # Ensure only one Admin can be created
    if role == 'Admin' and user.query.filter_by(role='Admin').first():
        return jsonify({'message': 'An admin already exists'}), 403

    # Check if username exists
    if user.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    # Create new user
    user = user(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': f'{role} registered successfully!'}), 201


@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Validate input
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Find user by username
    user = user.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Generate JWT token
    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({'message': 'Login successful', 'token': access_token}), 200


@auth_bp.route('/logout', methods=['POST'])
@cross_origin()
def logout():
    # JWT does not maintain session. For logout, you can blacklist the token or rely on frontend logic to clear it.
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/load_user', methods=['GET'])
@cross_origin()
def load_user():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token is missing'}), 403

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = user.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'user': {'id': user.id, 'email': user.email, 'role': user.role}}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
