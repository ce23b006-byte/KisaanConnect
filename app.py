from flask import Flask, render_template, request, jsonify, abort
from pathlib import Path
import json

BASE = Path(__file__).parent
app = Flask(__name__)

with open(BASE / "data" / "schemes.json", encoding="utf-8") as f:
    SCHEMES = json.load(f)

@app.get("/")
def home():
    states = sorted({s["state"] for s in SCHEMES if s["state"] != "All India"})
    crops = sorted({c for s in SCHEMES for c in s["crops"] if c != "All Crops"})
    return render_template("index.html", states=states, crops=crops)

@app.get("/api/schemes")
def search():
    query = request.args.get("q", "").strip().lower()
    state = request.args.get("state", "")
    crop = request.args.get("crop", "")
    category = request.args.get("category", "")
    results = []
    for s in SCHEMES:
        searchable = " ".join([
            s["name"], s["description"], s["benefit"], " ".join(s["tags"])
        ]).lower()
        if query and query not in searchable: continue
        if state and s["state"] not in ("All India", state): continue
        if crop and crop not in s["crops"] and "All Crops" not in s["crops"]: continue
        if category and s["category"] != category: continue
        results.append(s)
    return jsonify({"count": len(results), "schemes": results})

@app.get("/scheme/<int:scheme_id>")
def detail(scheme_id):
    scheme = next((s for s in SCHEMES if s["id"] == scheme_id), None)
    if not scheme: abort(404)
    return render_template("detail.html", scheme=scheme)

if __name__ == "__main__":
    app.run(debug=True)
