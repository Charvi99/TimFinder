# TimFinder

This project provides a simple flight tracking web service. It consists of a
Python/Flask backend that queries the [AviationStack](https://aviationstack.com/)
API for live flight data and a small front-end using Leaflet to display the
plane's position on a world map.

## Backend

The backend lives in `backend/` and exposes a single endpoint:

```
GET /api/flight/<flight_number>
```

The endpoint requires an API key for AviationStack. Set the environment variable
`AVIATIONSTACK_KEY` before running the server.

### Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### Run

```bash
export AVIATIONSTACK_KEY=your_key_here
python backend/app.py
```

## Frontend

Open `frontend/index.html` in a browser. Enter a flight number and the page will
request location data from the backend and place a marker on an interactive
map.
