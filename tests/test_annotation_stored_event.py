import uuid
from app.messaging.broker import RedisBroker

broker = RedisBroker()

event = {
    "topic": "annotation.stored",
    "event_id": f"evt_{uuid.uuid4().hex[:8]}",
    "payload": {
        "image_id": "img_002",
        "status": "stored"
    },
    "timestamp": "2026-05-01T00:00:00Z"
}

print("Publishing annotation.stored event...")
broker.publish("annotation.stored", event)
