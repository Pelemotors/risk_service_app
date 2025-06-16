from flask import Blueprint, request, jsonify
from models.financing_models import db, Customer
from datetime import datetime

customers_bp = Blueprint("customers", __name__)

@customers_bp.route("/customers", methods=["GET"])
def get_customers():
    """Get all customers"""
    try:
        customers = Customer.query.all()
        return jsonify({
            "success": True,
            "customers": [customer.to_dict() for customer in customers]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@customers_bp.route("/customers", methods=["POST"])
def create_customer():
    """Create a new customer"""
    try:
        data = request.get_json()
        
        # Basic validation
        required_fields = ["full_name", "id_number", "date_of_birth"]
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

        # Check if ID number already exists
        if Customer.query.filter_by(id_number=data["id_number"]).first():
            return jsonify({"success": False, "message": "Customer with this ID number already exists"}), 409

        customer = Customer(
            full_name=data.get("full_name"),
            id_number=data.get("id_number"),
            phone=data.get("phone"),
            email=data.get("email"),
            date_of_birth=datetime.strptime(data.get("date_of_birth"), 
                                             "%Y-%m-%d").date() if data.get("date_of_birth") else None,
            address=data.get("address"),
            marital_status=data.get("marital_status"),
            monthly_income=data.get("monthly_income"),
            monthly_expenses=data.get("monthly_expenses"),
            credit_score=data.get("credit_score"),
            employment_seniority=data.get("employment_seniority")
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "customer": customer.to_dict(),
            "message": "Customer created successfully"
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@customers_bp.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """Get a specific customer by ID"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify({
            "success": True,
            "customer": customer.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@customers_bp.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """Update a customer"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        data = request.get_json()
        
        for field in ["full_name", "id_number", "phone", "email", "address", 
                     "marital_status", "monthly_income", "monthly_expenses", 
                     "credit_score", "employment_seniority"]:
            if field in data:
                setattr(customer, field, data[field])
        
        if "date_of_birth" in data and data["date_of_birth"]:
            customer.date_of_birth = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()

        customer.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "customer": customer.to_dict(),
            "message": "Customer updated successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@customers_bp.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Delete a customer"""
    try:
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Customer deleted successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

