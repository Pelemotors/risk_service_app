#C:\GAL\financing\financing_app_backend\src\routes\risk_tiers.py
from flask import Blueprint, request, jsonify
from models.financing_models import db, RiskTier



risk_tiers_bp = Blueprint("risk_tiers", __name__)

@risk_tiers_bp.route("/risk_tiers", methods=["GET"])
def get_risk_tiers():
    """החזרת כל מדרגות הסיכון הקיימות"""
    try:
        tiers = RiskTier.query.order_by(RiskTier.min_score).all()
        return jsonify({
            "success": True,
            "risk_tiers": [tier.to_dict() for tier in tiers]
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@risk_tiers_bp.route("/risk_tiers", methods=["POST"])
def create_risk_tier():
    """יצירת מדרגת סיכון חדשה"""
    try:
        data = request.get_json()
        name = data.get("name")
        min_score = float(data.get("min_score"))
        max_score = float(data.get("max_score"))
        description = data.get("description")

        if not name or min_score is None or max_score is None:
            return jsonify({"success": False, "message": "שדות חובה חסרים"}), 400

        if RiskTier.query.filter_by(name=name).first():
            return jsonify({"success": False, "message": "שם מדרגה כבר קיים"}), 409

        # ✅ בדיקת חפיפה לטווחי ציונים
        overlapping = RiskTier.query.filter(
            (RiskTier.min_score <= max_score) & (RiskTier.max_score >= min_score)
        ).first()
        if overlapping:
            return jsonify({"success": False, "message": "טווח חופף למדרגה קיימת"}), 400

        tier = RiskTier(
            name=name,
            min_score=min_score,
            max_score=max_score,
            description=description
        )
        db.session.add(tier)
        db.session.commit()

        return jsonify({"success": True, "risk_tier": tier.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

@risk_tiers_bp.route("/risk_tiers/<int:tier_id>", methods=["GET"])
def get_risk_tier(tier_id):
    """החזרת מדרגת סיכון לפי מזהה"""
    try:
        tier = RiskTier.query.get_or_404(tier_id)
        return jsonify({"success": True, "risk_tier": tier.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@risk_tiers_bp.route("/risk_tiers/<int:tier_id>", methods=["PUT"])
def update_risk_tier(tier_id):
    """עדכון מדרגת סיכון"""
    try:
        tier = RiskTier.query.get_or_404(tier_id)
        data = request.get_json()

        name = data.get("name")
        min_score = float(data.get("min_score", tier.min_score))
        max_score = float(data.get("max_score", tier.max_score))
        description = data.get("description")

        if name:
            tier.name = name
        tier.min_score = min_score
        tier.max_score = max_score
        tier.description = description

        db.session.commit()
        return jsonify({
            "success": True,
            "risk_tier": tier.to_dict(),
            "message": "מדרגה עודכנה בהצלחה"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

@risk_tiers_bp.route("/risk_tiers/<int:tier_id>", methods=["DELETE"])
def delete_risk_tier(tier_id):
    """מחיקת מדרגת סיכון"""
    try:
        tier = RiskTier.query.get_or_404(tier_id)
        db.session.delete(tier)
        db.session.commit()
        return jsonify({"success": True, "message": "המדרגה נמחקה בהצלחה"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
