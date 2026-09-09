from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Backend is working!"
    }


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


def test_create_inspection():

    response = client.post(
        "/api/inspections",
        json={
            "product": "Biscuit",
            "mrp": 50,
            "quantity": "200g"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "inspection_id" in data
    assert data["status"] == "CREATED"
    assert data["data"]["product"] == "Biscuit"
    assert data["data"]["mrp"] == 50
    assert data["data"]["quantity"] == "200g"


def test_upload_image():

    create_response = client.post(
        "/api/inspections",
        json={
            "product": "Biscuit",
            "mrp": 50,
            "quantity": "200g"
        }
    )

    inspection_id = (
        create_response
        .json()["inspection_id"]
    )

    response = client.post(
        f"/api/inspections/{inspection_id}/images",
        files={
            "image": (
                "label.jpg",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["inspection_id"] == inspection_id
    assert data["filename"] == "label.jpg"
    assert data["message"] == "Image received"

    assert "m1_result" in data
    assert "m2_result" in data


def test_get_inspection():

    create_response = client.post(
        "/api/inspections",
        json={
            "product": "Biscuit",
            "mrp": 50,
            "quantity": "200g"
        }
    )

    inspection_id = (
        create_response
        .json()["inspection_id"]
    )

    client.post(
        f"/api/inspections/{inspection_id}/images",
        files={
            "image": (
                "label.jpg",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    response = client.get(
        f"/api/inspections/{inspection_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["inspection_id"] == inspection_id
    assert data["status"] == "COMPLETED"
    assert "m1_result" in data
    assert "m2_result" in data


def test_get_all_inspections():

    response = client.get(
        "/api/inspections"
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_dashboard():

    login_response = client.post(
        "/api/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/dashboard",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_inspections" in data
    assert "passed" in data
    assert "failed" in data
    assert "review" in data


def test_dashboard_without_token():

    response = client.get(
        "/api/dashboard"
    )

    assert response.status_code == 422


def test_dashboard_with_invalid_token():

    response = client.get(
        "/api/dashboard",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid or expired token"
    }


def test_login_success():

    response = client.post(
        "/api/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Login successful"
    assert data["username"] == "admin"
    assert data["role"] == "Admin"
    assert data["authenticated"] is True
    assert "access_token" in data


def test_login_failure():

    response = client.post(
        "/api/auth/login",
        json={
            "username": "admin",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Invalid username or password"
    assert data["authenticated"] is False
    assert data["access_token"] is None


def test_get_nonexistent_inspection():

    response = client.get(
        "/api/inspections/nonexistent-id"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Inspection not found"
    }


def test_upload_nonexistent_inspection():

    response = client.post(
        "/api/inspections/nonexistent-id/images",
        files={
            "image": (
                "label.jpg",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Inspection not found"
    }


def test_upload_unsupported_image():

    create_response = client.post(
        "/api/inspections",
        json={
            "product": "Biscuit",
            "mrp": 50,
            "quantity": "200g"
        }
    )

    inspection_id = (
        create_response
        .json()["inspection_id"]
    )

    response = client.post(
        f"/api/inspections/{inspection_id}/images",
        files={
            "image": (
                "label.txt",
                b"fake file content",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Unsupported image format"
    }


def test_upload_empty_filename():

    create_response = client.post(
        "/api/inspections",
        json={
            "product": "Biscuit",
            "mrp": 50,
            "quantity": "200g"
        }
    )

    inspection_id = (
        create_response
        .json()["inspection_id"]
    )

    response = client.post(
        f"/api/inspections/{inspection_id}/images",
        files={
            "image": (
                "",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_m1_contract():

    create_response = client.post(
        "/api/inspections",
        json={
            "product": "Biscuit",
            "mrp": 50,
            "quantity": "200g"
        }
    )

    inspection_id = (
        create_response
        .json()["inspection_id"]
    )

    response = client.post(
        f"/api/inspections/{inspection_id}/images",
        files={
            "image": (
                "label.jpg",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    m1 = response.json()["m1_result"]

    assert "image_id" in m1
    assert "quality" in m1
    assert "text_blocks" in m1
    assert "declarations" in m1
    assert "measurements" in m1

    assert m1["quality"]["status"] == "ACCEPTED"

    assert len(m1["text_blocks"]) > 0

    assert "mrp" in m1["declarations"]


def test_m2_contract():

    create_response = client.post(
        "/api/inspections",
        json={
            "product": "Biscuit",
            "mrp": 50,
            "quantity": "200g"
        }
    )

    inspection_id = (
        create_response
        .json()["inspection_id"]
    )

    response = client.post(
        f"/api/inspections/{inspection_id}/images",
        files={
            "image": (
                "label.jpg",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    m2 = response.json()["m2_result"]

    assert "rule_id" in m2
    assert "field" in m2
    assert "status" in m2
    assert "reason" in m2
    assert "confidence" in m2
    assert "evidence_regions" in m2
    assert "legal_reference" in m2

    assert m2["status"] in [
        "PASS",
        "FAIL",
        "REVIEW"
    ]


def test_m4_persistence():

    create_response = client.post(
        "/api/inspections",
        json={
            "product": "Biscuit",
            "mrp": 50,
            "quantity": "200g"
        }
    )

    inspection_id = (
        create_response
        .json()["inspection_id"]
    )

    client.post(
        f"/api/inspections/{inspection_id}/images",
        files={
            "image": (
                "label.jpg",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    response = client.get(
        f"/api/inspections/{inspection_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["inspection_id"] == inspection_id
    assert data["status"] == "COMPLETED"


def test_404_error_contract():

    response = client.get(
        "/api/inspections/does-not-exist"
    )

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data
    assert data["detail"] == "Inspection not found"


def test_health_endpoint():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_get_report():

    create_response = client.post(
        "/api/inspections",
        json={
            "product": "Biscuit",
            "mrp": 50,
            "quantity": "200g"
        }
    )

    assert create_response.status_code == 200

    inspection_id = (
        create_response
        .json()["inspection_id"]
    )

    upload_response = client.post(
        f"/api/inspections/{inspection_id}/images",
        files={
            "image": (
                "label.jpg",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    assert upload_response.status_code == 200

    response = client.get(
        f"/api/reports/{inspection_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["inspection_id"] == inspection_id
    assert data["status"] == "COMPLETED"
    assert data["filename"] == "label.jpg"

    assert "declarations" in data
    assert "compliance_result" in data
    assert "evidence" in data
    assert "report_file" in data

    assert "mrp" in data["declarations"]

    assert data["compliance_result"] is not None

    assert isinstance(
        data["evidence"],
        list
    )

    assert len(data["evidence"]) > 0

    assert data["evidence"][0]["region_id"] == "R01"

    assert data["report_file"] is None


def test_get_nonexistent_report():

    response = client.get(
        "/api/reports/nonexistent-id"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Inspection not found"
    }