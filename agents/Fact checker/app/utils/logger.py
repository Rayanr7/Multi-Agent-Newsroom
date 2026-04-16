import json
import os

LOG_FILE = "logs/runs.json"


def log_run(data: dict):
    os.makedirs("logs", exist_ok=True)

    # Ensure file exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    # Safe read
    try:
        with open(LOG_FILE, "r") as f:
            content = f.read().strip()
            logs = json.loads(content) if content else []
    except json.JSONDecodeError:
        logs = []  # fallback if corrupted

    # Append new log
    logs.append(data)

    # Write back
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)