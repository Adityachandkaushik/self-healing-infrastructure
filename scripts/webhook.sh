#!/bin/bash

echo "========================================="
echo "Starting Self-Healing Recovery..."
echo "========================================="

ansible-playbook \
-i ansible/inventory \
ansible/restart-nginx.yml

if [ $? -eq 0 ]; then
    echo "✅ Recovery completed successfully."
else
    echo "❌ Recovery failed."
    exit 1
fi