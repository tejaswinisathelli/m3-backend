def mock_m1(image_id: str):
    return {
        "image_id": image_id,
        "quality": {
            "status": "ACCEPTED",
            "score": 0.94
        },
        "text_blocks": [
            {
                "id": "R01",
                "text": "MRP ₹120",
                "confidence": 0.97,
                "bbox": [100, 200, 300, 240]
            }
        ],
        "declarations": {
            "mrp": {
                "value": 120,
                "currency": "INR",
                "confidence": 0.97,
                "source_regions": ["R01"]
            }
        },
        "measurements": []
    }


def process_with_m1(image_id: str):
    return mock_m1(image_id)