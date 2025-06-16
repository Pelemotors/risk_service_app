#C:\GAL\financing\financing_app_backend\Dockerfile
FROM python:3.12-slim

WORKDIR /app

# התקנת תלות למערכת (ל-Psycopg2 ועוד)
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=src/main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

CMD ["flask", "run"]
