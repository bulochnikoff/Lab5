import os
import requests
import threading
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv
from api import api
from database import db
from sqlalchemy import text
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5435/lab5db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CONSUL_URL'] = os.getenv('CONSUL_URL', 'http://consul:8500')

db.init_app(app)

with app.app_context():
    db.create_all()

api.init_app(app)

# Регистрация discovery blueprint
from api.discovery import bp as discovery_bp
app.register_blueprint(discovery_bp)

# Автоматическая регистрация в Consul при старте
def register_with_consul():
    try:
        service_id = f"backend-{os.getenv('HOSTNAME', 'default')}"
        address = "backend:5000"
        tags = ["api", "v1", "ml"]
        payload = {
            "id": service_id,
            "address": address,
            "tags": tags
        }
        resp = requests.post('http://backend:5000/discovery/register', json=payload, timeout=5)
        if resp.status_code == 200:
            logging.info("Successfully registered in Consul")
        else:
            logging.error(f"Failed to register: {resp.text}")
    except Exception as e:
        logging.error(f"Registration error: {e}")

threading.Timer(2.0, register_with_consul).start()

@app.route('/health', methods=['GET'])
def health():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)