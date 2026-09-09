mock_database = {}


def mock_m4_save(inspection_id: str, data: dict):
    if inspection_id in mock_database:
        mock_database[inspection_id].update(data)
    else:
        mock_database[inspection_id] = data

    return {
        "success": True,
        "inspection_id": inspection_id,
        "message": "Inspection saved successfully"
    }


def mock_m4_get(inspection_id: str):
    return mock_database.get(inspection_id)


def mock_m4_get_all():
    return list(mock_database.values())


def mock_m4_dashboard():
    total = len(mock_database)

    passed = 0
    failed = 0
    review = 0

    for inspection in mock_database.values():
        m2_result = inspection.get("m2_result")

        if m2_result:
            status = m2_result.get("status")

            if status == "PASS":
                passed += 1
            elif status == "FAIL":
                failed += 1
            elif status == "REVIEW":
                review += 1

    return {
        "total_inspections": total,
        "passed": passed,
        "failed": failed,
        "review": review
    }

def save_with_m4(inspection_id: str, data: dict):
    return mock_m4_save(inspection_id, data)


def get_with_m4(inspection_id: str):
    return mock_m4_get(inspection_id)


def get_all_with_m4():
    return mock_m4_get_all()


def get_dashboard_with_m4():
    return mock_m4_dashboard()