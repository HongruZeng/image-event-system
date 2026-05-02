import json

from app.messaging.broker import RedisBroker
from app.services.document_service import DocumentDBService
from app.models.events import create_event


def handle_inference_completed(event):
    payload = event["payload"]

    image_id = payload["image_id"]

    annotation = {
        "objects": payload.get("objects", []),
        "source": payload.get("source", "fake_inference")
    }

    db_service = DocumentDBService()
    saved_document = db_service.save_annotation(image_id, annotation)

    stored_event = create_event(
        "annotation.stored",
        {
            "image_id": image_id,
            "status": "stored"
        }
    )

    broker = RedisBroker()
    broker.publish("annotation.stored", stored_event)

    print("Saved to MongoDB:")
    print(saved_document)
    print("Published annotation.stored event:")
    print(stored_event)


def main():
    broker = RedisBroker()
    pubsub = broker.subscribe("inference.completed")

    print("Annotation Service is listening for inference.completed...")

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

        print("Received inference.completed event:")
        print(event)

        handle_inference_completed(event)


if __name__ == "__main__":
    main()

