import time
from app.messaging.broker import RedisBroker
from app.event_generator import generate_image_submitted_event


def main():
    broker = RedisBroker()

   
    event = generate_image_submitted_event(
        image_id="img_001",
        path="images/cat.jpg"
    )

    print("Publishing event:", event)

    broker.publish("image.submitted", event)


if __name__ == "__main__":
    main()
