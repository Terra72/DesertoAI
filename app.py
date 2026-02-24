from flask import Flask, jsonify, render_template
from db.repository import EventRepository

app = Flask(__name__)
repo = EventRepository()

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

if __name__ == "__main__":
    app.run(debug=True)