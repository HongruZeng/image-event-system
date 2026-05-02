from app.document_service import DocumentDBService


def main():
    service = DocumentDBService()

    annotation = {
        "objects": [
            {
                "label": "cat",
                "bbox": [10, 20, 100, 120],
                "conf": 0.95
            },
            {
                "label": "person",
                "bbox": [50, 60, 180, 220],
                "conf": 0.88
            }
        ],
        "source": "fake_inference"
    }

    saved = service.save_annotation("img_001", annotation)
    print("Saved annotation:")
    print(saved)

    found = service.get_annotation("img_001")
    print("Found annotation:")
    print(found)


if __name__ == "__main__":
    main()
