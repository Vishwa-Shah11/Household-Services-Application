from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes.admin_routes import admin_bp
from routes.customer_routes import customer_bp
from routes.professional_routes import professional_bp
from config import Config
from models import db, user, service, service_request

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(professional_bp)

    with app.app_context():
        db.init_app(app)
        db.create_all()  # Create tables

    @app.route('/')
    @app.route('/home')
    def home():
        return "Hello, Vishwa!"

    return app
    
if __name__ =='__main__':
    app = create_app()
    #db.create_all()
    app.run(host='0.0.0.0', port=5858, debug=True)



# app = Flask(__name__)
# app.config.from_object(Config)
# CORS(app)

# # Register Blueprints
# app.register_blueprint(admin_bp)
# app.register_blueprint(customer_bp)
# app.register_blueprint(professional_bp)

# with app.app_context():
#     db.init_app(app)
#     db.create_all()  # Create tables
    
# if __name__ == '__main__':
#     app.run(debug=True)
