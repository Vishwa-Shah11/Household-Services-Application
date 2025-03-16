from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.admin_routes import admin_bp
from routes.customer_routes import customer_bp
from routes.professional_routes import professional_bp
from routes.service_routes import service_bp
from config import Config
from models import db
from flask_login import LoginManager
from routes.auth import auth_bp
# import os
# from routes.professional_routes import UPLOAD_FOLDER

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect unauthorized users to login

    # Initialize JWT
    jwt = JWTManager(app) 

    CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Auth routes
    app.register_blueprint(admin_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(professional_bp)
    app.register_blueprint(service_bp, url_prefix='/service')

    # if not os.path.exists(UPLOAD_FOLDER):
    #     os.makedirs(UPLOAD_FOLDER)

    with app.app_context():
        db.init_app(app)
        # db.drop_all() #drop tables
        db.create_all()  # Create tables

    @app.route('/')
    @app.route('/home')
    def home():
        return "Hello!"

    return app
    
if __name__ =='__main__':
    app = create_app()
    # print(app.url_map)
    app.run(host='0.0.0.0', port=5858, debug=True)