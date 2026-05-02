from app.messaging.broker import RedisBroker
import json

def main():
    broker = RedisBroker()

    pubsub = broker.subscribe("image.submitted")

    print("Listening for messages...")

    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            print("Received event:", data)


if __name__ == "__main__":
    main()
