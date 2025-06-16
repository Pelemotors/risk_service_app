# C:\GAL\financing\financing_app_backend\src\main.py

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from flask import send_from_directory

from app_factory import create_app
from models.financing_models import db, User

app = create_app()

with app.app_context():
    db.create_all()

    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@financing.app',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created: admin/admin123")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    elif os.path.exists(os.path.join(static_folder_path, 'index.html')):
        return send_from_directory(static_folder_path, 'index.html')
    else:
        return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
