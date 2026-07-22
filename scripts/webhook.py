from flask import Flask, request, jsonify
import subprocess
import json
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Self-Healing Infrastructure Webhook",
        "status": "Running"
    })


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

    data = request.get_json()

    if not data:
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
            [
                "ansible-playbook",
                "-i",
                "ansible/inventory",
                "ansible/restart-nginx.yml"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        return jsonify({
            "status": "success",
            "message": "Recovery playbook executed successfully",
            "stdout": result.stdout
        }), 200

    except subprocess.CalledProcessError as e:

        return jsonify({
            "status": "failed",
            "message": "Recovery playbook execution failed",
            "stderr": e.stderr
        }), 500

    except Exception as e:

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