from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_booking():
    response = client.post(
        "/bookings/",
        json={
            "user_id": 1,
            "journey_id": 1,
            "status": "pending",
            "price": 20.0,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["journey_id"] == 1
    assert data["status"] == "pending"
    assert data["price"] == 20.0


def test_get_booking():
    booking_id = 1  # Assuming this ID exists for now
    response = client.get(f"/bookings/{booking_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == booking_id


def test_update_booking_status():
    booking_id = 1  # Assuming this ID exists for now
    response = client.put(
        f"/bookings/{booking_id}/status",
        json={"status": "confirmed"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"


def test_delete_booking():
    booking_id = 1  # Assuming this ID exists for now
    response = client.delete(f"/bookings/{booking_id}")
    assert response.status_code == 204