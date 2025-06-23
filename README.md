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
export AVIATIONSTACK_KEY=your_key_here  # Linux/macOS
python backend/app.py
```

If you are on Windows, use one of the following commands to set the
`AVIATIONSTACK_KEY` variable before running the backend:

```
set AVIATIONSTACK_KEY=your_key_here       # Command Prompt
$env:AVIATIONSTACK_KEY='your_key_here'    # PowerShell
```

Then start the application with `python backend/app.py`.

If a request fails with "Flight not found" it may mean the flight is not
currently in the air or that no live data is available from the API.

## Frontend

After the backend is running, open `http://localhost:5000/` in your browser.
Enter a flight number and the page will request location data from the backend
and place a marker on an interactive map.
