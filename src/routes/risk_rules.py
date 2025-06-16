from flask import Blueprint, request, jsonify
from models.financing_models import db, RiskRule
import json

risk_rules_bp = Blueprint("risk_rules", __name__)

@risk_rules_bp.route("/risk_rules", methods=["GET"])
def get_risk_rules():
    """Get all risk rules"""
    try:
        rules = RiskRule.query.all()
        return jsonify({
            "success": True,
            "risk_rules": [rule.to_dict() for rule in rules]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@risk_rules_bp.route("/risk_rules", methods=["POST"])
def create_risk_rule():
    """Create a new risk rule"""
    try:
        data = request.get_json()
        
        required_fields = ["name", "rule_json"]
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

        if RiskRule.query.filter_by(name=data["name"]).first():
            return jsonify({"success": False, "message": "Risk rule with this name already exists"}), 409

        # Validate rule_json is valid JSON
        try:
            json.loads(data["rule_json"])
        except json.JSONDecodeError:
            return jsonify({"success": False, "message": "Invalid JSON format for rule_json"}), 400

        rule = RiskRule(
            name=data.get("name"),
            description=data.get("description"),
            rule_json=data.get("rule_json"),
            weight=data.get("weight", 1.0),
            is_active=data.get("is_active", True)
        )
        
        db.session.add(rule)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "risk_rule": rule.to_dict(),
            "message": "Risk rule created successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@risk_rules_bp.route("/risk_rules/<int:rule_id>", methods=["GET"])
def get_risk_rule(rule_id):
    """Get a specific risk rule by ID"""
    try:
        rule = RiskRule.query.get_or_404(rule_id)
        return jsonify({
            "success": True,
            "risk_rule": rule.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@risk_rules_bp.route("/risk_rules/<int:rule_id>", methods=["PUT"])
def update_risk_rule(rule_id):
    """Update a risk rule"""
    try:
        rule = RiskRule.query.get_or_404(rule_id)
        data = request.get_json()
        
        for field in ["name", "description", "weight", "is_active"]:
            if field in data:
                setattr(rule, field, data[field])
        
        if "rule_json" in data:
            try:
                json.loads(data["rule_json"])
                rule.rule_json = data["rule_json"]
            except json.JSONDecodeError:
                return jsonify({"success": False, "message": "Invalid JSON format for rule_json"}), 400

        rule.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "risk_rule": rule.to_dict(),
            "message": "Risk rule updated successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@risk_rules_bp.route("/risk_rules/<int:rule_id>", methods=["DELETE"])
def delete_risk_rule(rule_id):
    """Delete a risk rule"""
    try:
        rule = RiskRule.query.get_or_404(rule_id)
        db.session.delete(rule)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Risk rule deleted successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

