from fastapi import FastAPI, HTTPException, Depends
from .db_provider import get_db, Session, text

# FastAPI app
app = FastAPI()

@app.get("/healthcheck")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"db_connection": "successful"}
    except Exception as e:
        return {"db_connection": "failed", "error": str(e)}