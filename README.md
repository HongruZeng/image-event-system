# 🚀 Image Event System

A simple event-driven system for image processing and vector search using a pub-sub architecture.

---

## 📦 Event Schema

All events follow a common structure:

```json
{
  "topic": "embedding.created",
  "event_id": "evt_123",
  "payload": {},
  "timestamp": "ISO-8601"
}
```

---

## ✅ Key Design Principles

### 1. Idempotency
Each event contains a unique `event_id`.

Duplicate events are safely ignored:

```
[SKIP] Duplicate event: evt_xxx
```

---

### 2. Robustness
Malformed or invalid events do not crash the system.

Examples:

```
[ERROR] Missing field: topic
[WARN] Invalid event rejected
```

---

### 3. Eventual Consistency
The system does not require strict ordering.

Example behavior:

```
Query arrives before embedding → empty results  
Embedding arrives → index updated  
Query again → correct results
```

---

## 🧠 System Architecture

- Annotation Service
- Embedding Service
- Vector Index Service

---

## 🚀 How to Run

### Start Services

```
PYTHONPATH=. python3 app/services/annotation_service.py
PYTHONPATH=. python3 app/services/embedding_service.py
PYTHONPATH=. python3 app/services/vector_index_service.py
```

---

### Run Tests

```
PYTHONPATH=. python3 tests/test_inference_event.py
PYTHONPATH=. python3 tests/test_duplicate_embedding.py
PYTHONPATH=. python3 tests/test_order.py
```

---

## 🎯 Conclusion

Event-driven + vector search + fault tolerance.
