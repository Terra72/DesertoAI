from flask import Flask, jsonify, render_template, request
from deserto.store.repository import EventRepository
from eval.taxonomy import REGIONS, TOPICS

app = Flask(__name__)
repo = EventRepository()

SIGNAL_TYPES = ["new", "reinforcement"]
FILTERS = {"region": REGIONS, "topic": TOPICS, "signal_type": SIGNAL_TYPES}
DEFAULT_LIMIT = 50
MAX_LIMIT = 200

# -------------------------
# Homepage (Map UI)
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# API: Latest region event
# -------------------------
@app.route("/region/<region>")
def region(region):
    event = repo.get_latest_by_region(region)

    if not event:
        return jsonify({"error": "No data"}), 404

    return jsonify({
        "title": event[0],
        "summary": event[1],
        "signal_type": event[2],
        "impact_direction": event[3],
        "timestamp": event[4]
    })

# -------------------------
# API: Events (filtered, newest first)
# -------------------------
@app.route("/api/events")
def api_events():
    filters = {name: request.args.get(name) for name in FILTERS}

    # Unknown filter values are a 400, not an empty list
    for name, value in filters.items():
        if value is not None and value not in FILTERS[name]:
            return jsonify({"error": f"Unknown {name}: {value}"}), 400

    try:
        limit = int(request.args.get("limit", DEFAULT_LIMIT))
    except ValueError:
        limit = 0
    if limit < 1:
        return jsonify({"error": "limit must be a positive integer"}), 400

    return jsonify(repo.get_events(limit=min(limit, MAX_LIMIT), **filters))

# -------------------------
# API: Event counts per region (parents include leaves)
# -------------------------
@app.route("/api/regions")
def api_regions():
    return jsonify(repo.count_by_region())

if __name__ == "__main__":
    app.run(debug=True)