from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from app.pendo_database import Booking  # Your ORM model

app = FastAPI()

DATABASE_URL = "mssql+pymssql://SA:reallyStrongPwd123@localhost:1433/Pendo.Database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BookingCreate(BaseModel):
    user_id: UUID
    journey_id: UUID
    price: Optional[float] = None


class BookingResponse(BaseModel):
    booking_id: UUID
    user_id: UUID
    journey_id: UUID
    status: str
    price: Optional[float] = None


@app.post("/bookings/", response_model=BookingResponse, status_code=201)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = Booking(
        UserId=booking.user_id,
        JourneyId=booking.journey_id,
        Status="pending",
        Price=booking.price,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return BookingResponse(
        booking_id=db_booking.BookingId,
        user_id=db_booking.UserId,
        journey_id=db_booking.JourneyId,
        status=db_booking.Status,
        price=db_booking.Price,
    )


@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: UUID, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.BookingId == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return BookingResponse(
        booking_id=db_booking.BookingId,
        user_id=db_booking.UserId,
        journey_id=db_booking.JourneyId,
        status=db_booking.Status,
        price=db_booking.Price,
    )


@app.put("/bookings/{booking_id}/status", response_model=BookingResponse)
def update_booking_status(booking_id: UUID, status_update: dict, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.BookingId == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if "status" not in status_update:
        raise HTTPException(status_code=400, detail="Missing status field")

    db_booking.Status = status_update["status"]
    db.commit()
    db.refresh(db_booking)

    return BookingResponse(
        booking_id=db_booking.BookingId,
        user_id=db_booking.UserId,
        journey_id=db_booking.JourneyId,
        status=db_booking.Status,
        price=db_booking.Price,
    )


@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: UUID, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.BookingId == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(db_booking)
    db.commit()


@app.get("/users/{user_id}/bookings", response_model=List[BookingResponse])
def get_bookings_by_user(user_id: UUID, db: Session = Depends(get_db)):
    user_bookings = db.query(Booking).filter(Booking.UserId == user_id).all()

    return [
        BookingResponse(
            booking_id=b.BookingId,
            user_id=b.UserId,
            journey_id=b.JourneyId,
            status=b.Status,
            price=b.Price,
        )
        for b in user_bookings
    ]