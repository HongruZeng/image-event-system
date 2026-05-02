import json
import uuid
from app.messaging.broker import RedisBroker

broker = RedisBroker()

event = {
    "topic": "inference.completed",
    "event_id": f"evt_{uuid.uuid4().hex[:8]}",
    "payload": {
        "image_id": "img_002",
        "objects": [
            {"label": "cat", "bbox": [10, 20, 100, 120], "conf": 0.95},
            {"label": "person", "bbox": [50, 60, 180, 220], "conf": 0.88}
        ],
        "source": "test_inference"
    },
    "timestamp": "2026-05-01T00:00:00Z"
}

print("🚀 Publishing inference.completed event...")
broker.publish("inference.completed", event)
