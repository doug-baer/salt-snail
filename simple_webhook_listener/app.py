#!/usr/bin/env python3
"""
Simple Flask app that receives a Salt-reactor webhook,
prints the JSON payload to stdout and appends it to a log file.
"""
import json
import os
from datetime import datetime, UTC
from pathlib import Path
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
LOG_DIR = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIR / "webhook.log"

# Make sure the log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)
def _write_log(entry: dict) -> None:

    """
    Append a JSON line to the logfile with a timestamp.
    """
    timestamp = datetime.now(UTC).isoformat() + "Z"
    #timestamp = datetime.utcnow().isoformat() + "Z"
    line = {"received_at": timestamp, "payload": entry}
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(line) + "\n")

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():

    """
    Expected: a JSON body (any shape).  Salt’s http.query sends a JSON string,
    but this endpoint will accept any valid JSON.
    """
    if not request.is_json:
        abort(400, description="Content-Type must be application/json")
    payload = request.get_json(silent=False)  # raise if malformed
    # --------------------------------------------------------------
    # Print to console (stdout) – useful for a live demo
    # --------------------------------------------------------------
    print("\n=== Salt webhook received ===")
    print(json.dumps(payload, indent=2))
    print("=============================\n")

    # --------------------------------------------------------------
    # Append to logfile
    # --------------------------------------------------------------
    _write_log(payload)

    # Respond with a tiny acknowledgement
    return jsonify({"status": "ok", "msg": "payload logged"}), 200

# ----------------------------------------------------------------------
# Health‑check endpoint (optional, handy for debugging)
# ----------------------------------------------------------------------
@app.route("/healthz", methods=["GET"])
def health():
    return "OK\n", 200
# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Run on all interfaces so Salt on another host can reach it.
    # In a demo you can also bind to 127.0.0.1 if everything runs locally.
    app.run(host="0.0.0.0", port=5000, debug=True)
