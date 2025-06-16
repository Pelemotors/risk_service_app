##C:\GAL\financing\financing_app_backend\risk_service\src\routes\risk_routes.py
from flask import Blueprint, jsonify, request
from models.risk_models import db, RiskRule, RiskTier


from datetime import datetime
import json

risk_rules_bp = Blueprint("risk_rules", __name__)

@risk_rules_bp.route("/risk_rules", methods=["GET"])
def get_risk_rules():
    try:
        rules = RiskRule.query.all()
        return jsonify({"success": True, "risk_rules": [r.to_dict() for r in rules]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@risk_rules_bp.route("/risk_rules", methods=["POST"])
def create_risk_rule():
    try:
        data = request.get_json()
        if not data.get("name") or not data.get("rule_json"):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        if RiskRule.query.filter_by(name=data["name"]).first():
            return jsonify({"success": False, "message": "Rule already exists"}), 409

        json.loads(data["rule_json"])  # Validate JSON

        rule = RiskRule(
            name=data["name"],
            description=data.get("description"),
            rule_json=data["rule_json"],
            weight=data.get("weight", 1.0),
            is_active=data.get("is_active", True)
        )

        db.session.add(rule)
        db.session.commit()
        return jsonify({"success": True, "risk_rule": rule.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
