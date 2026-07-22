from flask import Flask, request, jsonify
import subprocess
import json
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "application": "Self-Healing Infrastructure",
        "service": "Webhook",
        "status": "Running",
        "version": "1.0.0",
        "available_endpoints": [
            "/",
            "/health",
            "/webhook"
        ]
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "service": "Webhook",
        "version": "1.0.0",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200


@app.route("/webhook", methods=["POST"])
def webhook():

    # Validate JSON request
    if not request.is_json:
        return jsonify({
            "status": "failed",
            "message": "Content-Type must be application/json"
        }), 400

    data = request.get_json()

    if data is None:
        return jsonify({
            "status": "failed",
            "message": "No JSON payload received"
        }), 400

    print("\n" + "=" * 70)
    print("🚨 ALERT RECEIVED")
    print("=" * 70)
    print(json.dumps(data, indent=4))
    print("=" * 70)

    try:
        result = subprocess.run(
            ["bash", "scripts/webhook.sh"],
            capture_output=True,
            text=True,
            check=True
        )

        print("✅ Recovery Playbook Executed Successfully")

        return jsonify({
            "status": "success",
            "message": "Recovery playbook executed successfully",
            "stdout": result.stdout
        }), 200

    except subprocess.CalledProcessError as e:

        print("❌ Recovery Playbook Failed")

        return jsonify({
            "status": "failed",
            "message": "Recovery playbook execution failed",
            "stderr": e.stderr
        }), 500

    except Exception as e:

        print("❌ Unexpected Error:", str(e))

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )