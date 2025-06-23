import os
import requests
from flask import Flask, jsonify, abort

app = Flask(__name__)

API_KEY = os.environ.get("AVIATIONSTACK_KEY")
API_BASE = "http://api.aviationstack.com/v1/flights"

@app.route('/api/flight/<flight_number>')
def flight_info(flight_number):
    if not API_KEY:
        abort(500, description="API key not configured")
    params = {
        'access_key': API_KEY,
        'flight_iata': flight_number
    }
    resp = requests.get(API_BASE, params=params, timeout=10)
    if resp.status_code != 200:
        abort(resp.status_code)
    data = resp.json()
    flights = data.get('data', [])
    if not flights:
        abort(404, description="Flight not found")
    # Use the first flight entry
    flight = flights[0]
    position = flight.get('live', {})
    if not position:
        abort(404, description="No live data for this flight")
    return jsonify({
        'latitude': position.get('latitude'),
        'longitude': position.get('longitude'),
        'altitude': position.get('altitude')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
