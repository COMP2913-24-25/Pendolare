from pydantic import BaseModel

class StatusResponse(BaseModel):
    Status: str = "Success"
    Message: str = ""