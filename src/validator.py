REQUIRED_FIELDS = {"customer_id": str, "file_type": str, "records": int}
ALLOWED_FILE_TYPES = {"claim", "eligibility", "provider"}

def validate_payload(payload):
    errors = []
    if not isinstance(payload, dict):
        return False, ["Payload must be a JSON object."]

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in payload:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(payload[field], expected_type):
            errors.append(f"{field} must be of type {expected_type.__name__}")

    if isinstance(payload.get("customer_id"), str) and not payload["customer_id"].strip():
        errors.append("customer_id cannot be empty.")

    if isinstance(payload.get("file_type"), str) and payload["file_type"] not in ALLOWED_FILE_TYPES:
        errors.append("file_type must be claim, eligibility, or provider.")

    if isinstance(payload.get("records"), int) and payload["records"] < 0:
        errors.append("records cannot be negative.")

    return len(errors) == 0, errors
