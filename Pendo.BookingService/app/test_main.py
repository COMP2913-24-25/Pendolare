from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_booking():
    response = client.post(
        "/bookings/",
        json={
            "user_id": "e70c907b-70e8-4dd9-95cf-5e45c5d52f77",
            "journey_id": "ff589d93-89c0-4097-96a5-d9ef5e2be67a",
            "price": 20.0,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "e70c907b-70e8-4dd9-95cf-5e45c5d52f77"
    assert data["journey_id"] == "ff589d93-89c0-4097-96a5-d9ef5e2be67a"
    assert data["status"] == "pending"
    assert data["price"] == 20.0


def test_get_booking():
    booking_id = "e70c907b-70e8-4dd9-95cf-5e45c5d52f77"  # Replace with a real UUID if needed
    response = client.get(f"/bookings/{booking_id}")
    assert response.status_code == 200


def test_update_booking_status():
    booking_id = "e70c907b-70e8-4dd9-95cf-5e45c5d52f77"
    response = client.put(
        f"/bookings/{booking_id}/status",
        json={"status": "confirmed"},
    )
    assert response.status_code == 200


def test_delete_booking():
    booking_id = "e70c907b-70e8-4dd9-95cf-5e45c5d52f77"
    response = client.delete(f"/bookings/{booking_id}")
    assert response.status_code == 204