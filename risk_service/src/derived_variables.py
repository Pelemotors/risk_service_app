#C:\GAL\financing\financing_app_backend\risk_service\src\derived_variables.py
from datetime import datetime

def calculate_derived_variables(customer_data: dict) -> dict:
    derived = {}

    # גיל
    try:
        birth_date = datetime.strptime(customer_data.get("main_birthDate", ""), "%Y-%m-%d")
        today = datetime.today()
        derived["age"] = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    except Exception:
        derived["age"] = None

    # ותק בעבודה
    try:
        start_date = datetime.strptime(customer_data.get("employment_start_date", ""), "%Y-%m-%d")
        derived["employment_years"] = (datetime.today() - start_date).days // 365
    except Exception:
        derived["employment_years"] = None

    # יחס מימון בפועל
    try:
        sale_price = float(customer_data.get("sale_price", 0))
        loan_amount = float(customer_data.get("financing_amount", 0))
        derived["financing_ratio"] = round(loan_amount / sale_price, 2) if sale_price > 0 else None
    except Exception:
        derived["financing_ratio"] = None

    # גיל הרכב
    try:
        reg_year = int(customer_data.get("registration_year", 0))
        derived["vehicle_age"] = datetime.today().year - reg_year
    except Exception:
        derived["vehicle_age"] = None

    # סכום תשלום חודשי מוערך לפי מספר תשלומים
    try:
        r = 0.099 / 12
        n = int(customer_data.get("num_of_payments", 0))
        P = float(customer_data.get("financing_amount", 0))
        if r > 0 and n > 0:
            monthly = (P * r) / (1 - (1 + r) ** -n)
            derived["estimated_monthly_payment"] = round(monthly)
    except Exception:
        derived["estimated_monthly_payment"] = None

    return derived
