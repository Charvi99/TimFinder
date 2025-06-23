diff --git a/README.md b/README.md
index fa5cbdd22bfdc70a61975046c44f194d3c04987e..fd7a8f34f1a1fe19b8b07f90e80c7f9a46f08d30 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,59 @@
-# TimFinder
+# TimFinder
+
+This project provides a simple flight tracking web service. It consists of a
+Python/Flask backend that queries the [OpenSky Network](https://opensky-network.org/)
+API for live flight data and a small front-end using Leaflet to display the
+plane's position on a world map.
+
+## Backend
+
+The backend lives in `backend/` and exposes a single endpoint:
+
+```
+GET /api/flight/<flight_number>
+```
+
+The endpoint uses the OpenSky `states/all` API filtered by flight callsign.
+No API key is required, but you may provide credentials for better rate limits
+via the `OPENSKY_USERNAME` and `OPENSKY_PASSWORD` environment variables.
+
+### Install dependencies
+
+```bash
+python3 -m venv venv
+source venv/bin/activate
+pip install -r backend/requirements.txt
+```
+
+### Run
+
+```bash
+python backend/app.py
+```
+
+If you have OpenSky credentials you can set them before running the backend:
+
+```bash
+export OPENSKY_USERNAME=your_username
+export OPENSKY_PASSWORD=your_password
+```
+
+On Windows use:
+
+```
+set OPENSKY_USERNAME=your_username       # Command Prompt
+set OPENSKY_PASSWORD=your_password
+$env:OPENSKY_USERNAME='your_username'    # PowerShell
+$env:OPENSKY_PASSWORD='your_password'
+```
+
+Then start the application with `python backend/app.py`.
+
+If a request fails with "Flight not found" it may mean the flight is not
+currently in the air or that no live data is available from OpenSky.
+
+## Frontend
+
+After the backend is running, open `http://localhost:5000/` in your browser.
+Enter a flight number and the page will request location data from the backend
+and place a marker on an interactive map.
