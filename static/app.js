var map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
}).addTo(map);

// Pin position [lat, lng] for each ADR-0004 region.
// global and multi-region have no place, so they sit in the Atlantic.
var COORDS = {
    "north-america": [45, -100],
    "south-america": [-15, -60],
    "africa": [0, 20],
    "north-asia": [60, 95],
    "east-asia": [35, 105],
    "europe": [53, 20],
    "oceania": [-20, 165],
    "middle-east": [28, 45],
    "sahel-west-africa": [14, 0],
    "horn-east-africa": [7, 42],
    "southern-africa": [-22, 24],
    "mediterranean-southern-europe": [39, 10],
    "mena": [27, 28],
    "central-asia": [43, 65],
    "south-east-asia": [8, 110],
    "australia": [-25, 134],
    "americas-drylands": [23, -102],
    "global": [10, -35],
    "multi-region": [-30, -15]
};

var info = document.getElementById("info");

// Escape feed text before putting it in innerHTML
function esc(text) {
    var div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// Pin radius grows with the square root of the count, muted pins are small
function radius(count, max) {
    return count ? 6 + 14 * Math.sqrt(count / max) : 5;
}

var hovered;

// Show the latest event for a region. Parents include their leaves.
function showLatest(region) {
    hovered = region;
    fetch("/api/events?limit=1&region=" + region)
    .then(response => {
        if (!response.ok) throw new Error(response.status);
        return response.json();
    })
    .then(events => {
        if (hovered !== region) return;
        var data = events[0];
        info.innerHTML = data
            ? "<b>" + esc(data.title) + "</b><br>" +
              esc(data.summary) + "<br><i>" +
              esc(data.signal_type) + "</i>"
            : "No events";
    })
    .catch(() => {
        if (hovered === region) info.textContent = "Could not load events";
    });
}

var panel = document.getElementById("panel");
var panelTitle = document.getElementById("panel-title");
var panelCount = document.getElementById("panel-count");
var panelBody = document.getElementById("panel-body");
var EVENT_LIMIT = 20;

// Create an element. Text goes in as textContent, so feed text is safe.
function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
}

// Only http(s) links, so a feed cannot inject a javascript: URL
function safeUrl(url) {
    try {
        var parsed = new URL(url);
        return /^https?:$/.test(parsed.protocol) ? parsed.href : null;
    } catch (e) {
        return null;
    }
}

// Published date, falling back to ingested. Null if neither parses.
function eventDate(event) {
    for (const raw of [event.published_at, event.ingested_at]) {
        var date = raw ? new Date(raw) : null;
        if (date && !isNaN(date)) return date;
    }
    return null;
}

function countText(shown, total) {
    var noun = total === 1 ? " event" : " events";
    return shown < total ? "Latest " + shown + " of " + total + noun : total + noun;
}

function eventCard(event) {
    var card = el("article", "event");
    card.appendChild(el("h3", "", event.title));

    // Fixture summaries equal the title, so skip the repeat
    if (event.summary && event.summary.trim() !== (event.title || "").trim()) {
        card.appendChild(el("p", "summary", event.summary));
    }

    var meta = el("div", "meta");
    if (event.signal_type) {
        var badge = el("span", "badge", event.signal_type);
        badge.dataset.signal = event.signal_type;
        meta.appendChild(badge);
    }
    if (event.topic) meta.appendChild(el("span", "topic", event.topic));

    var date = eventDate(event);
    if (date) {
        var time = el("time", "", date.toLocaleDateString(undefined,
            {year: "numeric", month: "short", day: "numeric"}));
        time.dateTime = date.toISOString();
        meta.appendChild(time);
    }

    var href = safeUrl(event.url);
    if (href) {
        var link = el("a", "", "Source");
        link.href = href;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        meta.appendChild(link);
    } else {
        meta.appendChild(el("span", "muted", "No source link"));
    }

    card.appendChild(meta);
    return card;
}

var opened;

// Open the side panel with recent events for a region. Parents include their leaves.
function showPanel(region, count) {
    opened = region;
    panelTitle.textContent = region;
    panelCount.textContent = "";
    panelBody.replaceChildren(el("p", "state", "Loading events..."));
    panel.hidden = false;

    fetch("/api/events?limit=" + EVENT_LIMIT + "&region=" + region)
    .then(response => {
        if (!response.ok) throw new Error(response.status);
        return response.json();
    })
    .then(events => {
        if (opened !== region) return;
        panelCount.textContent = countText(events.length, Math.max(count, events.length));
        panelBody.replaceChildren(...(events.length
            ? events.map(eventCard)
            : [el("p", "state", "No events for this region yet")]));
    })
    .catch(() => {
        if (opened !== region) return;
        panelBody.replaceChildren(el("p", "state error", "Could not load events"));
    });
}

document.getElementById("panel-close").addEventListener("click", () => {
    opened = null;
    panel.hidden = true;
});

fetch("/api/regions")
.then(response => {
    if (!response.ok) throw new Error(response.status);
    return response.json();
})
.then(counts => {
    var max = Math.max(1, ...Object.values(counts));

    // Biggest first, so small pins stay on top and hoverable
    var regions = Object.entries(counts)
        .filter(([region]) => COORDS[region])
        .sort((a, b) => b[1] - a[1]);

    for (const [region, count] of regions) {
        var marker = L.circleMarker(COORDS[region], {
            radius: radius(count, max),
            color: count ? "#8c3b00" : "#888",
            fillColor: count ? "#e8751a" : "#bbb",
            fillOpacity: count ? 0.7 : 0.3,
            weight: 2
        }).addTo(map);

        marker.bindTooltip(region + ": " + count);
        marker.on("mouseover", () => showLatest(region));
        marker.on("click", () => showPanel(region, count));
    }
})
.catch(() => {
    info.textContent = "Could not load regions";
});
