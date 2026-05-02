from app.messaging.broker import RedisBroker
from app.models.events import create_event

broker = RedisBroker()

query_event = create_event(
    topic="query.submitted",
    payload={
        "embedding": [0.7, 0.04, 0.98, 0.40, 0.57, 0.85, 0.12, 0.39],
        "top_k": 2
    }
)

embedding_event = create_event(
    topic="embedding.created",
    payload={
        "image_id": "img_order_test",
        "embedding": [0.7, 0.04, 0.98, 0.40, 0.57, 0.85, 0.12, 0.39],
        "dim": 8,
        "source": "order_test"
    }
)

print("Sending query first...")
broker.publish("query.submitted", query_event)

print("Sending embedding later...")
broker.publish("embedding.created", embedding_event)

print("Sending query again...")
broker.publish("query.submitted", query_event)
