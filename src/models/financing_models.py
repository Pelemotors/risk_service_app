#C:\GAL\financing\financing_app_backend\src\models\financing_models.py

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json
from db import db



class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='underwriter')  # admin, underwriter, sales_rep
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='submitted_by', lazy=True)
    loans = db.relationship('Loan', backref='managed_by', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    id_number = db.Column(db.String(20), unique=True, nullable=False) # תעודת זהות
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    date_of_birth = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text)
    marital_status = db.Column(db.String(20)) # מצב משפחתי
    monthly_income = db.Column(db.Numeric(10, 2)) # הכנסה חודשית
    monthly_expenses = db.Column(db.Numeric(10, 2)) # הוצאות חודשיות
    credit_score = db.Column(db.Integer) # דירוג BDI או חיווי אשראי
    employment_seniority = db.Column(db.Integer) # ותק בעבודה בשנים
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='customer', lazy=True)
    loans = db.relationship('Loan', backref='customer', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'id_number': self.id_number,
            'phone': self.phone,
            'email': self.email,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'address': self.address,
            'marital_status': self.marital_status,
            'monthly_income': float(self.monthly_income) if self.monthly_income else None,
            'monthly_expenses': float(self.monthly_expenses) if self.monthly_expenses else None,
            'credit_score': self.credit_score,
            'employment_seniority': self.employment_seniority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    submitted_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    loan_amount = db.Column(db.Numeric(10, 2), nullable=False) # סכום הלוואה מבוקש
    loan_term_months = db.Column(db.Integer, nullable=False) # תקופת הלוואה בחודשים
    
    vehicle_make = db.Column(db.String(50)) # יצרן רכב מבוקש
    vehicle_model = db.Column(db.String(50)) # דגם רכב מבוקש
    vehicle_year = db.Column(db.Integer) # שנתון רכב מבוקש
    
    status = db.Column(db.String(20), default='pending') # pending, approved, rejected, in_review, waiting_docs
    risk_score = db.Column(db.Integer) # ציון סיכון
    risk_tier = db.Column(db.String(10)) # מדרגת סיכון (A, B, C, D, E)
    underwriter_notes = db.Column(db.Text) # הערות חיתום
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'submitted_by_user_id': self.submitted_by_user_id,
            'loan_amount': float(self.loan_amount),
            'loan_term_months': self.loan_term_months,
            'vehicle_make': self.vehicle_make,
            'vehicle_model': self.vehicle_model,
            'vehicle_year': self.vehicle_year,
            'status': self.status,
            'risk_score': self.risk_score,
            'risk_tier': self.risk_tier,
            'underwriter_notes': self.underwriter_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False) # תלוש שכר, תדפיס בנק, ת.ז., רישיון נהיגה
    file_url = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'document_type': self.document_type,
            'file_url': self.file_url,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

class RiskRule(db.Model):
    __tablename__ = 'risk_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    rule_json = db.Column(db.Text, nullable=False) # JSON string of the rule logic
    weight = db.Column(db.Numeric(5, 2), default=1.0) # משקולת להשפעת הכלל על ציון הסיכון
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rule_json': json.loads(self.rule_json) if self.rule_json else None,
            'weight': float(self.weight),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class RiskTier(db.Model):
    __tablename__ = 'risk_tiers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False) # A, B, C, D, E
    min_score = db.Column(db.Integer, nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'min_score': self.min_score,
            'max_score': self.max_score,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    managed_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    loan_amount_approved = db.Column(db.Numeric(10, 2), nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), nullable=False) # ריבית
    loan_term_months_approved = db.Column(db.Integer, nullable=False)
    monthly_payment = db.Column(db.Numeric(10, 2), nullable=False)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    status = db.Column(db.String(20), default='active') # active, closed, defaulted
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'customer_id': self.customer_id,
            'managed_by_user_id': self.managed_by_user_id,
            'loan_amount_approved': float(self.loan_amount_approved),
            'interest_rate': float(self.interest_rate),
            'loan_term_months_approved': self.loan_term_months_approved,
            'monthly_payment': float(self.monthly_payment),
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='paid') # paid, pending, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'loan_id': self.loan_id,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'amount': float(self.amount),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

