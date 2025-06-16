# C:\GAL\financing\financing_app_backend\src\app_factory.py
from flask import Flask, send_from_directory
from flask_cors import CORS
from models.financing_models import db
from routes.user import user_bp
from routes.customers import customers_bp
from routes.applications import applications_bp
from routes.risk_rules import risk_rules_bp
from routes.risk_tiers import risk_tiers_bp
from db import db

import os

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config['SECRET_KEY'] = 'financing_app_secret_key_2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/financing_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(customers_bp, url_prefix='/api')
    app.register_blueprint(applications_bp, url_prefix='/api')
    app.register_blueprint(risk_rules_bp, url_prefix='/api')
    app.register_blueprint(risk_tiers_bp, url_prefix='/api')

    return app
