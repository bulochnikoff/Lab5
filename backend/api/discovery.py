from flask import Blueprint, request, jsonify, current_app
import requests
import os

bp = Blueprint('discovery', __name__, url_prefix='/discovery')

@bp.route('/register', methods=['POST'])
def register_service():
    data = request.json
    service_id = data['id']
    address = data['address']
    tags = data.get('tags', [])
    
    consul_url = f"{current_app.config['CONSUL_URL']}/v1/agent/service/register"
    service_name = os.getenv('SERVICE_NAME', 'analytics-service')
    host, port = address.split(':')
    payload = {
        "ID": service_id,
        "Name": service_name,
        "Address": host,
        "Port": int(port),
        "Tags": tags,
        "Check": {
            "HTTP": f"http://{address}/health",
            "Interval": "10s",
            "Timeout": "5s"
        }
    }
    try:
        resp = requests.put(consul_url, json=payload)
        resp.raise_for_status()
        return jsonify({"status": "registered"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/services', methods=['GET'])
def get_services():
    tag = request.args.get('tag')
    service_name = os.getenv('SERVICE_NAME', 'analytics-service')
    consul_url = f"{current_app.config['CONSUL_URL']}/v1/catalog/service/{service_name}"
    if tag:
        consul_url += f"?tag={tag}"
    try:
        resp = requests.get(consul_url)
        resp.raise_for_status()
        return jsonify(resp.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500