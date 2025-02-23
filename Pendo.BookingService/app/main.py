from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv
from app.Pendo_Database import User, Booking, Journey, UserType
from pydantic import BaseModel
from uuid import UUID

# Load environment variables from .env file
load_dotenv()

# FastAPI app
app = FastAPI()

# Database Configuration
DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"mssql+pymssql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Booking Service is Running!"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"db_connection": "successful"}
    except Exception as e:
        return {"db_connection": "failed", "error": str(e)}

# Pydantic models
class BookingCreate(BaseModel):
    user_id: UUID
    journey_id: UUID
    status: str = "pending"

class BookingResponse(BaseModel):
    booking_id: UUID
    user_id: UUID
    journey_id: UUID
    status: str

# Create a new booking
@app.post("/bookings/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = Booking(
        UserId=booking.user_id,
        JourneyId=booking.journey_id,
        Status=booking.status
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

# Get a booking by ID
@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: UUID, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.BookingId == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

# Update a booking status
@app.put("/bookings/{booking_id}/status", response_model=BookingResponse)
def update_booking_status(booking_id: UUID, status: str, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.BookingId == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db_booking.Status = status
    db.commit()
    db.refresh(db_booking)
    return db_booking

# Delete a booking
@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: UUID, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.BookingId == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
    return