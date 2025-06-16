# C:\GAL\financing\financing_app_backend\seed_risk_tiers.py


import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
sys.path.insert(0, SRC_DIR)

from app_factory import create_app
from models.financing_models import db, RiskTier

app = create_app()

risk_tiers_data = [
    {"name": "A", "min_score": 0.0, "max_score": 2.0, "description": "סיכון נמוך מאוד"},
    {"name": "B", "min_score": 2.01, "max_score": 4.5, "description": "סיכון נמוך"},
    {"name": "C", "min_score": 4.51, "max_score": 7.1, "description": "סיכון בינוני"},
    {"name": "D", "min_score": 7.11, "max_score": 9.5, "description": "סיכון בינוני גבוה"},
    {"name": "E", "min_score": 9.51, "max_score": 15.0, "description": "סיכון גבוה"},
    {"name": "F", "min_score": 15.1, "max_score": 25.0, "description": "סיכון גבוה מאוד"},
    {"name": "G", "min_score": 25.01, "max_score": 100.0, "description": "סיכון קיצוני"},
]

with app.app_context():
    for data in risk_tiers_data:
        exists = RiskTier.query.filter_by(name=data["name"]).first()
        if not exists:
            tier = RiskTier(**data)
            db.session.add(tier)
    db.session.commit()
    print("✅ מדרגות הסיכון נוספו בהצלחה.")
