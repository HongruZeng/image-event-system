# 🚀 Event-Driven Image Vector Search System

A lightweight event-driven system for image processing and vector similarity search.

---

## 🎯 Motivation

Traditional pipelines tightly couple components (annotation → embedding → search).

This project redesigns the system using an **event-driven architecture**:

- Loose coupling between services
- Asynchronous processing
- Better scalability and robustness

---

## 🧠 Architecture

Inference → Annotation Service → Embedding Service → Vector Index Service

Communication is handled via Redis Pub/Sub.

---

## 🔑 Key Design Principles

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

## ⚙️ Components

### Annotation Service
- Listens to `inference.completed`
- Publishes `annotation.stored`

### Embedding Service
- Generates embeddings
- Publishes `embedding.created`

### Vector Index Service
- Stores embeddings (FAISS)
- Handles search queries

---

## 🚀 How to Run

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

## 🧪 What This Project Shows

- Event-driven architecture
- Pub/Sub messaging
- Vector similarity search
- Fault-tolerant design
- Eventual consistency

---

## 🏁 Conclusion

This project demonstrates how to build a scalable, decoupled, and robust event-driven system for visual search.
