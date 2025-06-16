#C:\GAL\financing\financing_app_backend\risk_service\Dockerfile
FROM python:3.12-slim

# תיקיית העבודה בתוך הקונטיינר
WORKDIR /app/src

# התקנת תלויות מערכת (למקרה שנעבוד עם PostgreSQL או נרצה קומפילציה)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# העתקת קובץ הדרישות והתקנת ספריות פייתון
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד המקור לתוך הקונטיינר
COPY src/ .


# משתני סביבה
ENV FLASK_APP=src/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# תיקון עיקרי – הגדרת PYTHONPATH כדי שפייתון יזהה את המודול src
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# הפקודה שמריצה את האפליקציה
CMD ["flask", "run"]
