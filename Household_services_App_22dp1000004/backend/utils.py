from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] != required_role:
                return jsonify({'message': 'Access forbidden: insufficient permissions'}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
