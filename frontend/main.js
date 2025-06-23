const form = document.getElementById('flight-form');
const mapDiv = document.getElementById('map');
let map;

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const flightNumber = document.getElementById('flight-number').value;
    try {
        const resp = await fetch(`/api/flight/${flightNumber}`);
        const data = await resp.json();
        if (!resp.ok) {
            throw new Error(data.description || 'Flight not found');
        }

        const { latitude, longitude } = data;
        if (!map) {
            map = L.map('map').setView([latitude, longitude], 6);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: '&copy; OpenStreetMap contributors'
            }).addTo(map);
        }
        map.setView([latitude, longitude], 6);
        L.marker([latitude, longitude]).addTo(map);
    } catch (err) {
        alert(err.message);
    }
});
