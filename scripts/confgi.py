import os

WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", 5001))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ANSIBLE_INVENTORY = os.getenv("ANSIBLE_INVENTORY", "ansible/inventory")
ANSIBLE_PLAYBOOK = os.getenv("ANSIBLE_PLAYBOOK", "ansible/restart-nginx.yml")
API_KEY = os.getenv("API_KEY", "change-me")