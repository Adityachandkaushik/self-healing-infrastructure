import os
import json
import subprocess
from datetime import datetime

from flask import Flask, request, jsonify, render_template
from logger import logger

# ==========================
# Base Directory
# ==========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# ==========================
# Dashboard
# ==========================

@app.route("/", methods=["GET"])
def home():

    logs = [
        "Webhook Server Running",
        "Prometheus Connected",
        "Grafana Connected",
        "Alertmanager Running",
        "Node Exporter Healthy",
        "Recovery Engine Ready"
    ]

    return render_template(
        "index.html",
        logs=logs
    )


# ==========================
# Health Check
# ==========================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "UP",
        "service": "Webhook",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })


# ==========================
# Webhook Endpoint
# ==========================

@app.route("/webhook", methods=["POST"])
def webhook():

    if not request.is_json:

        logger.warning("Invalid Content-Type")

        return jsonify({
            "status": "failed",
            "message": "Content-Type must be application/json"
        }), 400

    data = request.get_json()

    if not data:

        logger.warning("No JSON payload received")

        return jsonify({
            "status": "failed",
            "message": "No JSON payload received"
        }), 400

    alerts = data.get("alerts", [])

    if not alerts:

        logger.warning("No alerts found")

        return jsonify({
            "status": "failed",
            "message": "No alerts found"
        }), 400

    alert_name = alerts[0]["labels"].get("alertname", "Unknown")

    logger.info("=" * 70)
    logger.info(f"Alert Received : {alert_name}")
    logger.info(json.dumps(data, indent=4))
    logger.info("=" * 70)

    try:

        logger.info("Executing recovery script...")

        result = subprocess.run(
            ["bash", "scripts/webhook.sh"],
            capture_output=True,
            text=True,
            check=True
        )

        logger.info("Recovery Successful")

        return jsonify({
            "status": "success",
            "alert": alert_name,
            "message": "Recovery completed successfully",
            "stdout": result.stdout,
            "timestamp": datetime.now().isoformat()
        })

    except subprocess.CalledProcessError as e:

        logger.error("Recovery Failed")
        logger.error(e.stderr)

        return jsonify({
            "status": "failed",
            "alert": alert_name,
            "stderr": e.stderr,
            "timestamp": datetime.now().isoformat()
        }), 500

    except Exception as e:

        logger.exception("Unexpected Error")

        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# ==========================
# Start Server
# ==========================

if __name__ == "__main__":

    logger.info("Webhook server started on port 5001")

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    ) 