import uuid
from app.messaging.broker import RedisBroker

broker = RedisBroker()

event_id = f"evt_{uuid.uuid4().hex[:8]}"

event = {
    "topic": "embedding.created",
    "event_id": event_id,
    "payload": {
        "image_id": "img_duplicate_test",
        "embedding": [0.1] * 8,
        "dim": 8,
        "source": "duplicate_test"
    },
    "timestamp": "2026-05-01T00:00:00Z"
}

print("Publishing the same embedding.created event twice...")
broker.publish("embedding.created", event)
broker.publish("embedding.created", event)

print("\n--- Testing malformed event ---")
broker.publish("embedding.created", {"bad": "data"})
