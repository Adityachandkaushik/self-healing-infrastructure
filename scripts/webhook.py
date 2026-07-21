from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    print("=" * 60)
    print("Alert Received")
    print(json.dumps(data, indent=2))
    print("=" * 60)

    try:
        subprocess.run(
            [
                "ansible-playbook",
                "-i",
                "ansible/inventory",
                "ansible/restart-nginx.yml"
            ],
            check=True
        )

        return jsonify({
            "status": "success",
            "message": "Recovery playbook executed successfully"
        }), 200

    except subprocess.CalledProcessError as e:

        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500


@app.route("/", methods=["GET"])
def home():
    return "Webhook Server Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)