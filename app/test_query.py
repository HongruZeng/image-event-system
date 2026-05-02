from app.messaging.broker import RedisBroker
from app.models.events import create_event


def main():
    broker = RedisBroker()

    event = create_event(
        "query.submitted",
        {
            "query_image_id": "img_002",
            "top_k": 3
        }
    )

    broker.publish("query.submitted", event)

    print("Published query.submitted event:")
    print(event)


if __name__ == "__main__":
    main()
