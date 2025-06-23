import os
import requests
from flask import Flask, jsonify, abort, send_from_directory
from werkzeug.exceptions import HTTPException


app = Flask(__name__)

API_KEY = os.environ.get("AVIATIONSTACK_KEY")
API_BASE = "https://api.aviationstack.com/v1/flights"
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')


@app.errorhandler(HTTPException)
def handle_http_error(e):
    """Return JSON responses for all HTTP errors."""
    response = jsonify({'description': e.description})
    response.status_code = e.code or 500
    return response



@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/main.js')
def main_js():
    return send_from_directory(FRONTEND_DIR, 'main.js')


@app.route('/favicon.ico')
def favicon():
    # Return empty response to avoid 404 warnings in logs
    return '', 204

@app.route('/api/flight/<flight_number>')
def flight_info(flight_number):
    if not API_KEY:
        abort(500, description="API key not configured")

    params = {
        'access_key': API_KEY,
        'flight_iata': flight_number,
        'limit': 1
    }

    try:
        resp = requests.get(API_BASE, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        abort(502, description="Error contacting AviationStack")

    data = resp.json()

    if 'error' in data:
        abort(502, description=data['error'].get('message', 'API error'))

    flights = data.get('data', [])
    if not flights:
        abort(404, description="Flight not found")

    # Use the first flight entry
    flight = flights[0]
    position = flight.get('live')
    if not position:
        abort(404, description="No live data for this flight")

    return jsonify({
        'latitude': position.get('latitude'),
        'longitude': position.get('longitude'),
        'altitude': position.get('altitude')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
