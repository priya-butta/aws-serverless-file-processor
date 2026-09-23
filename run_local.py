import json
import logging
from src.handler import INCOMING_DIR, lambda_handler

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

sample = {
    "customer_id": "C1001",
    "file_type": "claim",
    "records": 12
}

INCOMING_DIR.mkdir(parents=True, exist_ok=True)
path = INCOMING_DIR / "sample_event.json"
path.write_text(json.dumps(sample, indent=2), encoding="utf-8")

response = lambda_handler({"file_name": path.name})
print(json.dumps(response, indent=2))
