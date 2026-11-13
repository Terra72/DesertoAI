var map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
}).addTo(map);

// You will later replace this with real geojson boundaries
var regions = {
    africa: [0, 20],
    europe: [50, 10],
    asia: [30, 90],
    australia: [-25, 135],
    north_america: [40, -100],
    south_america: [-15, -60]
};

for (const [region, coords] of Object.entries(regions)) {
    var marker = L.marker(coords).addTo(map);

    marker.on("mouseover", function() {
        fetch("/region/" + region)
        .then(response => response.json())
        .then(data => {
            document.getElementById("info").innerHTML =
                "<b>" + data.title + "</b><br>" +
                data.summary + "<br><i>" +
                data.signal_type + "</i>";
        });
    });
}
