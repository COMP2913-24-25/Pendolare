from pydantic import BaseModel

class DbConfiguration(BaseModel):
    db_server="localhost:1433"
    db_database="Pendo.Database"
    db_username="SA"
    db_password="YourPassword123"