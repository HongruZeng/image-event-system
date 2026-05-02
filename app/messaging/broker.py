import json
import os
import redis
from dotenv import load_dotenv

from app.models.events import validate_event


load_dotenv()


class RedisBroker:
    def __init__(self):
        host = os.getenv("REDIS_HOST")
        port = os.getenv("REDIS_PORT")
        password = os.getenv("REDIS_PASSWORD")

        if not host or not port or not password:
            raise ValueError("Redis configuration is missing. Check your .env file.")

        self.client = redis.Redis(
            host=host,
            port=int(port),
            password=password,
            decode_responses=True
        )

    def publish(self, topic, event):
        try:
            if not validate_event(event):
                print("[WARN] Invalid event rejected")
                return

            self.client.publish(topic, json.dumps(event))

        except Exception as e:
            print(f"[ERROR] Failed to publish: {e}")

    def subscribe(self, topic):
        pubsub = self.client.pubsub()
        pubsub.subscribe(topic)
        return pubsub
