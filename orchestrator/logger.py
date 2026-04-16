import json
import os

# Use an absolute path for the log file relative to the package root
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(ROOT_DIR, "logs", "runs.json")

def log_event(data):
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r+") as f:
        logs = json.load(f)
        logs.append(data)
        f.seek(0)
        json.dump(logs, f, indent=4)
