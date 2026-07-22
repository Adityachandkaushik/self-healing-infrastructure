import subprocess
from logger import logger

def execute_playbook(playbook, inventory):
    logger.info(f"Running playbook: {playbook}")

    result = subprocess.run(
        [
            "ansible-playbook",
            "-i",
            inventory,
            playbook
        ],
        capture_output=True,
        text=True
    )

    return result