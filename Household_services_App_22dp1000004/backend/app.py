from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.admin_routes import admin_bp
from routes.customer_routes import customer_bp
from routes.professional_routes import professional_bp
from routes.service_routes import service_bp
from config import Config, CeleryConfig, init_cache
from models import db
from flask_login import LoginManager
from routes.auth import auth_bp
from worker import celery_init_app
import flask_excel as excel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Initialize JWT
    jwt = JWTManager(app) 

    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Auth routes
    app.register_blueprint(admin_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(professional_bp)
    app.register_blueprint(service_bp, url_prefix='/service')

    # Initialize Redis Cache
    init_cache(app)

    with app.app_context():
        db.init_app(app)
        celery_init_app(app, CeleryConfig)
        excel.init_excel(app)

        # db.drop_all() #drop tables
        db.create_all()  # Create tables

    @app.route('/')
    @app.route('/home')
    def home():
        return "Hello!"

    return app
    
if __name__ =='__main__':
    app = create_app()
    celery_app = app.extensions["celery"]
    # print(app.url_map)
    app.run(host='0.0.0.0', port=5858, debug=True)