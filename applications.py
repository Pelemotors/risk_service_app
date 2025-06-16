from flask import Blueprint, request, jsonify
from models.financing_models import db, Application, Customer, User
from datetime import datetime

applications_bp = Blueprint("applications", __name__)

@applications_bp.route("/applications", methods=["GET"])
def get_applications():
    """Get all applications"""
    try:
        applications = Application.query.all()
        return jsonify({
            "success": True,
            "applications": [app.to_dict() for app in applications]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@applications_bp.route("/applications", methods=["POST"])
def create_application():
    """Create a new application"""
    try:
        data = request.get_json()
        
        required_fields = ["customer_id", "submitted_by_user_id", "loan_amount", "loan_term_months"]
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

        # Basic validation for customer and user existence
        customer = Customer.query.get(data["customer_id"])
        if not customer:
            return jsonify({"success": False, "message": "Customer not found"}), 404
        
        user = User.query.get(data["submitted_by_user_id"])
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        application = Application(
            customer_id=data.get("customer_id"),
            submitted_by_user_id=data.get("submitted_by_user_id"),
            loan_amount=data.get("loan_amount"),
            loan_term_months=data.get("loan_term_months"),
            vehicle_make=data.get("vehicle_make"),
            vehicle_model=data.get("vehicle_model"),
            vehicle_year=data.get("vehicle_year"),
            status=data.get("status", "pending"),
            risk_score=data.get("risk_score"),
            risk_tier=data.get("risk_tier"),
            underwriter_notes=data.get("underwriter_notes")
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "application": application.to_dict(),
            "message": "Application created successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@applications_bp.route("/applications/<int:application_id>", methods=["GET"])
def get_application(application_id):
    """Get a specific application by ID"""
    try:
        application = Application.query.get_or_404(application_id)
        return jsonify({
            "success": True,
            "application": application.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@applications_bp.route("/applications/<int:application_id>", methods=["PUT"])
def update_application(application_id):
    """Update an application"""
    try:
        application = Application.query.get_or_404(application_id)
        data = request.get_json()
        
        for field in ["loan_amount", "loan_term_months", "vehicle_make", 
                     "vehicle_model", "vehicle_year", "status", 
                     "risk_score", "risk_tier", "underwriter_notes"]:
            if field in data:
                setattr(application, field, data[field])

        application.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "application": application.to_dict(),
            "message": "Application updated successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@applications_bp.route("/applications/<int:application_id>", methods=["DELETE"])
def delete_application(application_id):
    """Delete an application"""
    try:
        application = Application.query.get_or_404(application_id)
        db.session.delete(application)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Application deleted successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

