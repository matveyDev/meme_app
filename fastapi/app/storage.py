import json
import os
from typing import Dict

DATA_FILE = "wallets.json"

def load_data() -> Dict[str, Dict]:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data: Dict[str, Dict]):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
