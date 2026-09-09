def mock_m2(m1_result):
    return {
        "rule_id": "PCR_XXXX",
        "field": "mrp",
        "status": "REVIEW",
        "reason": "Mock compliance result",
        "confidence": 0.90,
        "evidence_regions": ["R01"],
        "legal_reference": "Mock legal reference"
    }


def process_with_m2(m1_result):
    return mock_m2(m1_result)