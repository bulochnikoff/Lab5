import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from api import api
from database import db
import logging

load_dotenv()

app = Flask(__name__)

# Конфигурация БД
database_url = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/lab3db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Создание таблиц (один раз)
with app.app_context():
    db.create_all()

# Подключение Swagger
api.init_app(app)

# Логирование запросов 
logging.basicConfig(level=logging.INFO)

@app.after_request
def log_request(response):
    logging.info(f"{request.method} {request.path} -> {response.status_code}")
    return response

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)