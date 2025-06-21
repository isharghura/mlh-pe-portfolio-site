document.addEventListener('DOMContentLoaded', function () {
    // init map
    const map = L.map('map').setView([20, 0], 2);

    // add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // get locs from data attribute
    const mapElement = document.getElementById('map');
    const locations = JSON.parse(mapElement.dataset.locations);

    // add markers
    locations.forEach(loc => {
        L.marker([loc.lat, loc.lng])
            .addTo(map)
            .bindPopup(`<b>${loc.name}</b>`);
    });
});