import json
import numpy as np
import faiss

from app.messaging.broker import RedisBroker
from app.models.events import create_event
from app.services.embedding_service import generate_fake_embedding

class VectorIndexService:
    def __init__(self, dim=8):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.image_ids = []
        self.processed_events = set()

    def add_embedding(self, event):
        event_id = event["event_id"]

        if event_id in self.processed_events:
            print(f"[SKIP] Duplicate event:{event_id}")
            return

        payload = event["payload"]
        image_id = payload["image_id"]
        embedding = payload["embedding"]

        vector = np.array([embedding], dtype="float32")
        self.index.add(vector)
        self.image_ids.append(image_id)
        self.processed_events.add(event_id)

        print(f"Added embedding for {image_id}")

    def handle_query(self, event):
        payload = event["payload"]

        query_embedding = payload["embedding"]
        top_k = payload.get("top_k", 3)

        results = self.search(query_embedding, top_k)

        print("Search results:")
        print(results)

    def search(self, query_embedding, top_k=3):
        if len(self.image_ids) == 0:
            return []

        vector = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(vector, top_k)

        results = []

        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue

            results.append({
                "image_id": self.image_ids[idx],
                "distance": float(distance)
            })

        return results


def main():
    broker = RedisBroker()
    vector_service = VectorIndexService()

    pubsub = broker.client.pubsub()
    pubsub.subscribe("embedding.created", "query.submitted")

    print("Vector Index Service is listening for embedding.created and query.submitted...")

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

        topic = event["topic"]
        payload = event["payload"]

        if topic == "embedding.created":
            if "image_id" not in payload:
                print("[ERROR] Missing image_id")
                continue

            if "embedding" not in payload:
                print("[ERROR] Missing embedding")
                continue

            print("Received embedding.created event:")
            print(event)

            try:
                vector_service.add_embedding(event)
            except Exception as e:
                print("[ERROR] Failed to add embedding:", e)

        elif topic == "query.submitted":
            if "embedding" not in payload:
                print("[ERROR] Missing query embedding")
                continue

            print("Received query.submitted event:")
            print(event)

            try:
                vector_service.handle_query(event)
            except Exception as e:
                print("[ERROR] Failed to handle query:", e)


if __name__ == "__main__":
    main()
