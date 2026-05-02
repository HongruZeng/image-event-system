from datetime import datetime, timezone
import uuid


VALID_TOPICS = {
    "image.submitted",
    "inference.completed",
    "annotation.stored",
    "embedding.created",
    "query.submitted",
    "query.completed",
}


def create_event(topic, payload):
    if topic not in VALID_TOPICS:
        raise ValueError("Invalid topic")

    event = {
        "topic": topic,
        "event_id": "evt_" + uuid.uuid4().hex[:8],
        "payload": payload,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return event


def validate_event(event):
    required_fields = ["topic", "event_id", "payload", "timestamp"]

    if not isinstance(event, dict):
        return False

    for field in required_fields:
        if field not in event:
            print(f"[ERROR] Missing field: {field}")
            return False

    if not isinstance(event["payload"], dict):
        print("[ERROR] payload must be a dict")
        return False

    return True
