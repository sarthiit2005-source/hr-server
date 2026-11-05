
from flask import Flask, request, jsonify
from datetime import datetime, timezone
import os
import json

app = Flask(__name__)

FILE_PATH = "/home/data/hr_links.jsonl"

@app.route("/hr_link", methods=["POST"])
def save_hr_link():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"accept": "false"}), 400

    link = data.get("link")

    if not isinstance(link, str) or not link.strip():
        return jsonify({"accept": "false"}), 400

    entry = {
        "link": link,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

        with open(FILE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    except OSError:
        return jsonify({"accept": "false"}), 500

    return jsonify({"accept": "true"})
