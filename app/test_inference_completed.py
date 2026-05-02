from app.messaging.broker import RedisBroker
from app.models.events import create_event


def main():
    broker = RedisBroker()

    event = create_event(
        "inference.completed",
        {
            "image_id": "img_002",
            "objects": [
                {
                    "label": "car",
                    "bbox": [12, 44, 188, 200],
                    "conf": 0.93
                },
                {
                    "label": "person",
                    "bbox": [230, 51, 286, 210],
                    "conf": 0.88
                }
            ],
            "source": "fake_inference"
        }
    )

    broker.publish("inference.completed", event)

    print("Published inference.completed event:")
    print(event)


if __name__ == "__main__":
    main()
