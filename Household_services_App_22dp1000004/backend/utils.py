from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
import jwt

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

def get_customer_id_from_token(token):
    try:
        secret_key = "your_secret_key"  # Replace with your actual secret key
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        # print("Decoded Token:", decoded_token)
        # Extract user ID from 'sub'
        user_data = decoded_token.get("sub")  # sub contains {"id": 2, "role": "Customer"}
        if not user_data or "id" not in user_data:
            print("User ID not found in token")
            return None

        customer_id = user_data["id"]
        # print(f"Found Customer ID: {customer_id}")
        return customer_id
    except jwt.ExpiredSignatureError:
        print("Token Expired")
        return None  # Token expired
    except jwt.InvalidTokenError as e:
        print(f"Invalid Token: {e}")
        return None  # Invalid token