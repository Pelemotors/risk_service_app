# financing_app_backend/risk_service/src/risk_engine.py

from typing import Dict, List
from derived_variables import calculate_derived_variables  # ✅ חישוב משתנים נגזרים
from models.risk_models import RiskTier  # ✅ מודל טבלת מדרגות איכות
from sqlalchemy.orm.exc import MultipleResultsFound

def calculate_risk_score(customer_data: Dict, rules: List[Dict]) -> Dict:
    total_score = 0.0
    matched_rules = []

    # ✅ חישוב משתנים נגזרים ועדכון הנתונים
    derived = calculate_derived_variables(customer_data)
    customer_data.update(derived)

    # ✅ הרצת הכללים
    for rule in rules:
        rule_name = rule["name"]
        condition = rule["condition"]
        weight = rule.get("weight", 0)

        try:
            if eval(condition, {}, customer_data):
                total_score += weight
                matched_rules.append({
                    "rule": rule_name,
                    "weight": weight
                })
        except Exception as e:
            print(f"שגיאה בבדיקת כלל '{rule_name}': {e}")

    # ✅ קבלת מדרגת סיכון מתוך טבלת DB
    grade = get_risk_tier_from_db(total_score)

    return {
        "score": round(total_score, 2),
        "grade": grade,
        "matched_rules": matched_rules
    }


def get_risk_tier_from_db(score: float) -> str:
    """
    מחזיר את שם מדרגת הסיכון הרלוונטית עבור ציון סיכון נתון.
    """
    try:
        tier = RiskTier.query.filter(
            RiskTier.min_score <= score,
            RiskTier.max_score >= score
        ).first()
        return tier.name if tier else "לא ידוע"
    except MultipleResultsFound:
        return "שגיאה: מדרגות חופפות"
    except Exception as e:
        print(f"שגיאה בשליפת מדרגת סיכון: {e}")
        return "שגיאה"

