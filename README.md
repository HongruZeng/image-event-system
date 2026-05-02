# Image Event System

An event-driven system for processing image inference results and performing vector similarity search.

This project demonstrates how to build a **decoupled, fault-tolerant pipeline** using Redis Pub/Sub and FAISS.

---

## Overview

Instead of building a tightly coupled pipeline, this system uses an **event-driven architecture**:

- Services communicate via events
- Each component is independent
- The system tolerates failures and out-of-order execution

---

## Architecture

Inference → Annotation Service → Embedding Service → Vector Index Service

Communication is handled via Redis Pub/Sub.

---

## Components

### 1. Annotation Service
- Listens to: `inference.completed`
- Extracts objects from inference results
- Publishes: `annotation.stored`

---

### 2. Embedding Service
- Listens to: `annotation.stored`
- Generates embeddings (currently fake)
- Publishes: `embedding.created`

---

### 3. Vector Index Service
- Listens to:
  - `embedding.created`
  - `query.submitted`
- Stores vectors using FAISS
- Performs similarity search

---

##  Key Design Principles

### Idempotency
Each event has a unique `event_id`.

Duplicate events are safely ignored:
```
[SKIP] Duplicate event: evt_xxx
```

---

### Robustness
Malformed events do not crash the system:
```
[ERROR] Missing field: topic
[WARN] Invalid event rejected
```

---

### Eventual Consistency
The system does not require strict ordering.

Example:
```
Query → empty result  
Embedding → index updated  
Query again → correct result
```

---

## How to Run

Start services (3 terminals):

```
PYTHONPATH=. python3 app/services/annotation_service.py
PYTHONPATH=. python3 app/services/embedding_service.py
PYTHONPATH=. python3 app/services/vector_index_service.py
```

---

Run tests:

```
PYTHONPATH=. python3 tests/test_inference_event.py
PYTHONPATH=. python3 tests/test_duplicate_embedding.py
PYTHONPATH=. python3 tests/test_order.py
```

---

## What This Project Shows

- Event-driven architecture
- Pub/Sub messaging
- Vector similarity search
- Fault-tolerant design
- Eventual consistency

---

## 🏁 Conclusion

This project demonstrates how to build a scalable, decoupled, and robust event-driven system for visual search.
