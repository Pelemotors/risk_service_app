##C:\GAL\financing\financing_app_backend\risk_service\src\routes\risk_calculation_routes.py
from flask import Blueprint, request, jsonify
from models.risk_models import db, RiskRule, RiskTier


from risk_engine import calculate_risk_score
import json

# הגדרת ה-Blueprint עבור /api/risk
risk_calc_bp = Blueprint("risk_calc", __name__)

@risk_calc_bp.route("/calculate", methods=["POST"])
def calculate_risk():
    try:
        # קבלת נתוני לקוח מה-Body של הבקשה
        customer_data = request.get_json()
        if not customer_data or not isinstance(customer_data, dict):
            return jsonify({"success": False, "message": "Missing or invalid customer data"}), 400

        # שליפת כל החוקים הפעילים מה-DB
        active_rules = RiskRule.query.filter_by(is_active=True).all()
        if not active_rules:
            return jsonify({"success": False, "message": "No active rules found"}), 500

        # המרה לפורמט שמנוע הסיכון צריך
        parsed_rules = []
        for rule in active_rules:
            try:
                rule_data = json.loads(rule.rule_json)
                parsed_rules.append({
                    "name": rule.name,
                    "condition": rule_data.get("condition", ""),
                    "weight": rule.weight
                })
            except Exception as e:
                print(f"שגיאה בפענוח חוק {rule.name}: {e}")

        # חישוב הציון בפועל
        result = calculate_risk_score(customer_data, parsed_rules)

        return jsonify({
            "success": True,
            "input": customer_data,
            "matched_rules": result.get("matched_rules", []),
            "score": result.get("score"),
            "grade": result.get("grade")
        })

    except Exception as e:
        print(f"שגיאה כללית בחישוב: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
