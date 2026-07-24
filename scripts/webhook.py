import subprocess
import requests
from pathlib import Path
from datetime import datetime

from flask import Flask, jsonify, render_template, request

from logger import logger

# ==========================================================
# Configuration
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROMETHEUS_URL = "http://localhost:9091"
ALERTMANAGER_URL = "http://localhost:9093"

WEBHOOK_SCRIPT = BASE_DIR / "scripts" / "webhook.sh"

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

RECOVERY_LOG = LOG_DIR / "recovery.log"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

# ==========================================================
# Helper
# ==========================================================

def log_recovery(alert_name, status):

    with open(RECOVERY_LOG, "a") as file:

        file.write(
            f"{datetime.now()} | {alert_name} | {status}\n"
        )


def query_prometheus(query):

    try:

        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": query},
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        result = data.get("data", {}).get("result", [])

        if not result:
            return None

        return float(result[0]["value"][1])

    except Exception as e:

        logger.error(f"Prometheus Error : {e}")

        return None


# ==========================================================
# Metrics
# ==========================================================

def get_cpu_usage():

    value = query_prometheus(
        '100-(avg(rate(node_cpu_seconds_total{mode="idle"}[1m]))*100)'
    )

    return round(value, 2) if value is not None else 0


def get_memory_usage():

    value = query_prometheus(
        '(1-node_memory_MemAvailable_bytes/node_memory_MemTotal_bytes)*100'
    )

    return round(value, 2) if value is not None else 0


def get_disk_usage():

    value = query_prometheus(
        '100-((node_filesystem_avail_bytes{fstype!="tmpfs"}*100)/node_filesystem_size_bytes{fstype!="tmpfs"})'
    )

    return round(value, 2) if value is not None else 0


# ==========================================================
# Health
# ==========================================================

def get_prometheus_status():

    try:

        response = requests.get(
            f"{PROMETHEUS_URL}/-/healthy",
            timeout=3
        )

        return "UP" if response.status_code == 200 else "DOWN"

    except:

        return "DOWN"


def get_alertmanager_status():

    try:

        response = requests.get(
            f"{ALERTMANAGER_URL}/-/healthy",
            timeout=3
        )

        return "UP" if response.status_code == 200 else "DOWN"

    except:

        return "DOWN"


# ==========================================================
# Alerts
# ==========================================================

def get_active_alerts():

    try:

        response = requests.get(
            f"{ALERTMANAGER_URL}/api/v2/alerts",
            timeout=5
        )

        response.raise_for_status()

        alerts = response.json()

        active = []

        for alert in alerts:

            if alert["status"]["state"] == "active":

                active.append({

                    "name": alert["labels"].get("alertname", "Unknown"),

                    "severity": alert["labels"].get("severity", "N/A"),

                    "state": alert["status"]["state"]

                })

        return active

    except Exception as e:

        logger.error(e)

        return []


# ==========================================================
# Recovery History
# ==========================================================

def get_history():

    if not RECOVERY_LOG.exists():

        return []

    with open(RECOVERY_LOG) as file:

        return [line.strip() for line in file.readlines()][-20:]

        # ==========================================================
# Routes
# ==========================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():

    return jsonify({

        "status": "healthy",

        "prometheus": get_prometheus_status(),

        "alertmanager": get_alertmanager_status(),

        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    })


@app.route("/metrics")
def metrics():

    alerts = get_active_alerts()

    return jsonify({

        "cpu": get_cpu_usage(),

        "memory": get_memory_usage(),

        "disk": get_disk_usage(),

        "prometheus": get_prometheus_status(),

        "alertmanager": get_alertmanager_status(),

        "active_alerts": len(alerts),

        "alerts": alerts,

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    })


@app.route("/history")
def history():

    return jsonify({

        "history": get_history()

    })


# ==========================================================
# Webhook
# ==========================================================

@app.route("/webhook", methods=["POST"])
def webhook():

    try:

        payload = request.get_json(force=True)

        logger.info("Webhook received")

        alerts = payload.get("alerts", [])

        if not alerts:

            return jsonify({

                "status": "ignored",

                "message": "No alerts"

            }), 200

        alert = alerts[0]

        alert_name = alert.get("labels", {}).get(

            "alertname",

            "Unknown Alert"

        )

        severity = alert.get("labels", {}).get(

            "severity",

            "unknown"

        )

        logger.info(

            f"Alert : {alert_name} | Severity : {severity}"

        )
        try:

            logger.info("Executing recovery script...")

            result = subprocess.run(
                ["bash", str(WEBHOOK_SCRIPT)],
                capture_output=True,
                text=True,
                check=True
            )

            logger.info(result.stdout)

            log_recovery(
                alert_name,
                "SUCCESS"
            )

            return jsonify({

                "status": "success",

                "alert": alert_name,

                "severity": severity,

                "message": "Recovery completed successfully",

                "output": result.stdout

            }), 200

        except subprocess.CalledProcessError as e:

            logger.error(e.stderr)

            log_recovery(
                alert_name,
                "FAILED"
            )

            return jsonify({

                "status": "failed",

                "alert": alert_name,

                "severity": severity,

                "message": "Recovery failed",

                "error": e.stderr

            }), 500

    except Exception as e:

        logger.exception(e)

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500


        # ==========================================================
# Application Entry Point
# ==========================================================

if __name__ == "__main__":

    logger.info("=" * 60)
    logger.info("Self-Healing Infrastructure Webhook Started")
    logger.info(f"Prometheus    : {PROMETHEUS_URL}")
    logger.info(f"Alertmanager  : {ALERTMANAGER_URL}")
    logger.info(f"Recovery Log  : {RECOVERY_LOG}")
    logger.info("=" * 60)

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )