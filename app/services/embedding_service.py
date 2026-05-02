import json
import random

from app.messaging.broker import RedisBroker
from app.models.events import create_event


def generate_fake_embedding(image_id, dim=8):
    random.seed(image_id)

    embedding = []
    for _ in range(dim):
        embedding.append(random.random())

    return embedding


def handle_annotation_stored(event):
    payload = event["payload"]
    image_id = payload["image_id"]

    embedding = generate_fake_embedding(image_id)

    embedding_event = create_event(
        "embedding.created",
        {
            "image_id": image_id,
            "embedding": embedding,
            "dim": len(embedding),
            "source": "fake_embedding"
        }
    )

    broker = RedisBroker()
    broker.publish("embedding.created", embedding_event)

    print("Generated fake embedding:")
    print(embedding)

    print("Published embedding.created event:")
    print(embedding_event)


def main():
    broker = RedisBroker()
    pubsub = broker.subscribe("annotation.stored")

    print("Embedding Service is listening for annotation.stored...")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            event = json.loads(message["data"])
        except Exception as e:
            print("[ERROR] Bad JSON:", e)
            continue

        if "payload" not in event:
            print("[ERROR] No payload")
            continue

        if "image_id" not in event["payload"]:
            print("[ERROR] Missing image_id in payload")
            continue

        print("Received annotation.stored event:")
        print(event)

        handle_annotation_stored(event)


if __name__ == "__main__":
    main()
