# Image Event System (EC530 Project)

## 📌 Overview

This project implements an **event-driven visual object retrieval system** using a **pub-sub architecture**.

The system processes images, generates embeddings, stores them in a vector index, and supports similarity search using top-k nearest neighbors.

The goal is to design the **system architecture, messaging flow, and robustness**, rather than focusing on AI models.

---

## 🏗️ System Architecture

The system is composed of multiple independent services communicating via a message broker (Redis Pub/Sub):


CLI / Test Scripts
↓
Redis Broker
├── image.submitted
├── inference.completed
├── annotation.stored
├── embedding.created
├── query.submitted
↓
Services:

Annotation Service
Embedding Service
Vector Index Service (FAISS)

---

## 🔄 Event Flow

### 1. Image Processing Pipeline


image.submitted
↓
inference.completed
↓
annotation.stored
↓
embedding.created
↓
Vector Index updated


---

### 2. Query Flow


query.submitted
↓
Vector Index Service
↓
Top-K similar images returned


---

## 🧱 Components

### 1. Messaging System
- Redis Pub/Sub used as event broker
- Topics:
  - `image.submitted`
  - `inference.completed`
  - `annotation.stored`
  - `embedding.created`
  - `query.submitted`

---

### 2. Annotation Service
- Listens to: `inference.completed`
- Stores annotation in MongoDB
- Publishes: `annotation.stored`

---

### 3. Embedding Service
- Listens to: `annotation.stored`
- Generates embedding (mocked)
- Publishes: `embedding.created`

---

### 4. Vector Index Service
- Listens to:
  - `embedding.created`
  - `query.submitted`
- Uses FAISS for vector similarity search
- Supports top-k retrieval

---

## 🧾 Event Schema

All events follow a common structure:

```json
{
  "topic": "embedding.created",
  "event_id": "evt_123",
  "payload": {...},
  "timestamp": "ISO-8601"
}
⚙️ Key Design Principles
✅ Idempotency

Each event contains a unique event_id.

Duplicate events are safely ignored:

[SKIP] Duplicate event: evt_xxx

This ensures no duplicate writes or inconsistent state.

✅ Robustness

Malformed or invalid events do not crash the system.

Examples:

[ERROR] Missing field: topic
[WARN] Invalid event rejected
✅ Eventual Consistency

The system does not require strict ordering.

Example behavior:

Query arrives before embedding → empty results
Embedding arrives → index updated
Query again → correct results

This demonstrates eventual consistency.

✅ Loose Coupling
Services do not call each other directly
Communication only via events
Easy to extend and scale
🔍 Vector Search
Implemented using FAISS (IndexFlatL2)
Supports:
Adding embeddings
Top-k nearest neighbor search

Example output:

Search results:
[{'image_id': 'img_002', 'distance': 0.0}]
🧪 Testing
1. Duplicate Event Test
test_duplicate_embedding.py

Verifies idempotency.

2. Malformed Event Test
test_duplicate_embedding.py

Verifies robustness.

3. Event Ordering Test
test_order.py

Verifies eventual consistency.

🚀 How to Run
Start Services (separate terminals)
PYTHONPATH=. python3 app/services/annotation_service.py
PYTHONPATH=. python3 app/services/embedding_service.py
PYTHONPATH=. python3 app/services/vector_index_service.py
Run Tests
PYTHONPATH=. python3 tests/test_inference_event.py
PYTHONPATH=. python3 tests/test_duplicate_embedding.py
PYTHONPATH=. python3 tests/test_order.py
⚠️ Important Notes
CLI and tests must not access databases directly
All communication goes through services
System tolerates:
duplicate events
malformed events
out-of-order events
📈 Future Improvements
Replace fake embedding with real model
Use persistent vector database (e.g., Pinecone)
Add REST API layer
Add monitoring/logging
🏁 Conclusion

This project demonstrates how to build a robust, scalable event-driven system for visual search using:

Pub-Sub architecture
Vector similarity search
Fault-tolerant design
Eventual consistency
