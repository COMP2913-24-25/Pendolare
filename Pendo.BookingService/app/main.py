from fastapi import FastAPI, HTTPException, Depends
from .db_provider import get_db, Session, text

app = FastAPI(
    title="Pendo.BookingService.Api", 
    version="1.0.0",
    root_path="/api")

@app.get("/HealthCheck", tags=["HealthCheck"])
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"db_connection": "successful"}
    except Exception as e:
        return {"db_connection": "failed", "error": str(e)}

@app.post("/GetBookings", tags=["Get Bookings"])
def get_bookings(db: Session = Depends(get_db)):
    return {}

@app.post("/CreateBooking", tags=["Create Bookings"])
def create_booking(db: Session = Depends(get_db)):
    return {}

@app.post("/UpdateBooking", tags=["Update Bookings"])
def update_booking(db: Session = Depends(get_db)):
    return {}