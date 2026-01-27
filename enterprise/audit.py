import json
import time
from pathlib import Path

AUDIT_FILE = Path("audit_log.jsonl")


def log_action(actor: str, role: str, action: str, metadata: dict = None):
    entry = {
        "timestamp": int(time.time()),
        "actor": actor,
        "role": role,
        "action": action,
        "metadata": metadata or {},
    }

    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
