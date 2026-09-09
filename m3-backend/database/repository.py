inspections = {}


def save_inspection(inspection_id: str, data: dict):
    inspections[inspection_id] = data


def get_inspection(inspection_id: str):
    return inspections.get(inspection_id)


def get_all_inspections():
    return list(inspections.values())


def get_dashboard_data():
    total = len(inspections)

    passed = 0
    failed = 0
    review = 0

    for inspection in inspections.values():
        status = inspection["m2_result"]["status"]

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





