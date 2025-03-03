from pydantic import BaseModel

class GetJourneysRequest(BaseModel):
    OrderByPrice: bool
    StartLat: float
    StartLong: float
    EndLat: float
    end_long: float
    BootHeight : float
    BootWidth : float
    #ADD MORE FILTERS