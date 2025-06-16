##C:\GAL\financing\financing_app_backend\risk_service\src\main.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # ✅ תמיכה ב-CORS

from routes.risk_routes import risk_rules_bp
from routes.risk_calculation_routes import risk_calc_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "static"))  # ✅ שורת תיקון
CORS(app)  # ✅ מאפשר קבלת בקשות מכל דומיין (לצורך פיתוח)

# Database config - שימוש ב-SQLite לפיתוח מקומי
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///risk_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Register blueprints
app.register_blueprint(risk_rules_bp, url_prefix="/api")
app.register_blueprint(risk_calc_bp, url_prefix="/api/risk")

# Initialize tables
with app.app_context():
    from models.risk_models import RiskRule, RiskTier
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
