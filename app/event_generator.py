from app.models.events import create_event


def generate_image_submitted_event(image_id, path, source="user_upload"):
    payload = {
        "image_id": image_id,
        "path": path,
        "source": source,
    }

    return create_event("image.submitted", payload)
