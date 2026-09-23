from pathlib import Path
import json
import logging
import shutil
from src.validator import validate_payload

LOGGER = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parents[1]
INCOMING_DIR = BASE_DIR / "data" / "incoming"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REJECTED_DIR = BASE_DIR / "data" / "rejected"

def ensure_directories():
    for directory in (INCOMING_DIR, PROCESSED_DIR, REJECTED_DIR):
        directory.mkdir(parents=True, exist_ok=True)

def process_file(file_path):
    ensure_directories()
    path = Path(file_path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        destination = REJECTED_DIR / path.name
        shutil.move(str(path), destination)
        LOGGER.error("Could not read %s: %s", path.name, exc)
        return {"status": "rejected", "file": path.name, "errors": [str(exc)]}

    is_valid, errors = validate_payload(payload)
    if is_valid:
        destination = PROCESSED_DIR / path.name
        status = "processed"
    else:
        destination = REJECTED_DIR / path.name
        status = "rejected"

    shutil.move(str(path), destination)
    return {"status": status, "file": path.name, "errors": errors}

def lambda_handler(event, context=None):
    ensure_directories()
    file_name = event.get("file_name")
    if not file_name:
        return {"statusCode": 400, "body": {"message": "file_name is required"}}

    incoming_file = INCOMING_DIR / file_name
    if not incoming_file.exists():
        return {"statusCode": 404, "body": {"message": f"{file_name} not found"}}

    result = process_file(incoming_file)
    return {"statusCode": 200 if result["status"] == "processed" else 422, "body": result}
