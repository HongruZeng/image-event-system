from app.messaging.broker import RedisBroker
from app.models.events import create_event

broker = RedisBroker()

event = create_event(
    topic="query.submitted",
    payload={
        "embedding": [0.7580605916169291, 0.04213811891740693, 0.9858403376769131, 0.4076503452348673, 0.5785463810828965, 0.8581781013673095, 0.12683403358566347, 0.39054000221397467],
        "top_k": 2
    }
)

print("Publishing query.submitted event...")
broker.publish("query.submitted", event)
