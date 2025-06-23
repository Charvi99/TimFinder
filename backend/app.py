import os
import requests
from flask import Flask, jsonify, abort, send_from_directory
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

OPENSKY_USERNAME = os.environ.get("OPENSKY_USERNAME")
OPENSKY_PASSWORD = os.environ.get("OPENSKY_PASSWORD")
API_BASE = "https://opensky-network.org/api/states/all"
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
    """Return the location of the plane with the given callsign."""
    auth = None
    if OPENSKY_USERNAME and OPENSKY_PASSWORD:
        auth = (OPENSKY_USERNAME, OPENSKY_PASSWORD)

    try:
        resp = requests.get(API_BASE, auth=auth, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        abort(502, description="Error contacting OpenSky")

    try:
        data = resp.json()
    except ValueError:
        abort(502, description="Invalid response from OpenSky")

    states = data.get('states') or []
    search = flight_number.strip().upper()
    match = None
    for state in states:
        callsign = (state[1] or '').strip().upper()
        if callsign == search:
            match = state
            break

    if not match:
        abort(404, description="Flight not found")

    latitude = match[6]
    longitude = match[5]
    altitude = match[13] if match[13] is not None else match[7]

    return jsonify({
        'latitude': latitude,
        'longitude': longitude,
        'altitude': altitude
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)