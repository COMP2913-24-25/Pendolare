from fastapi.testclient import TestClient
from app.main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Pendo_Database import Base, Booking
from uuid import uuid4
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a new database session for testing
DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"mssql+pymssql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the testing database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_booking():
    response = client.post(
        "/bookings/",
        json={
            "user_id": str(uuid4()),
            "journey_id": str(uuid4()),
            "status": "pending"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "booking_id" in data
    assert data["status"] == "pending"

def test_get_booking():
    # First, create a booking to retrieve
    response = client.post(
        "/bookings/",
        json={
            "user_id": str(uuid4()),
            "journey_id": str(uuid4()),
            "status": "pending"
        },
    )
    booking_id = response.json()["booking_id"]

    # Now, retrieve the booking
    response = client.get(f"/bookings/{booking_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["booking_id"] == booking_id

def test_update_booking_status():
    # First, create a booking to update
    response = client.post(
        "/bookings/",
        json={
            "user_id": str(uuid4()),
            "journey_id": str(uuid4()),
            "status": "pending"
        },
    )
    booking_id = response.json()["booking_id"]

    # Now, update the booking status
    response = client.put(
        f"/bookings/{booking_id}/status",
        json={"status": "confirmed"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"

def test_delete_booking():
    # First, create a booking to delete
    response = client.post(
        "/bookings/",
        json={
            "user_id": str(uuid4()),
            "journey_id": str(uuid4()),
            "status": "pending"
        },
    )
    booking_id = response.json()["booking_id"]

    # Now, delete the booking
    response = client.delete(f"/bookings/{booking_id}")
    assert response.status_code == 204

    # Verify the booking is deleted
    response = client.get(f"/bookings/{booking_id}")
    assert response.status_code == 404