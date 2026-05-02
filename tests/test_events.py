from app.event_generator import generate_image_submitted_event


def test_create_event():
    event = generate_image_submitted_event(
        image_id="img_001",
        path="images/cat.jpg"
    )

    assert event["topic"] == "image.submitted"
    assert "event_id" in event
    assert "payload" in event
    assert "timestamp" in event
    assert event["payload"]["image_id"] == "img_001"
def test_invalid_event():
    bad_event = {
        "topic": "wrong.topic",
        "payload": {"image_id": "img_001"},
        "timestamp": "2026-04-07T14:33:00Z"
    }

    from app.models.events import validate_event

    assert validate_event(bad_event) is False
