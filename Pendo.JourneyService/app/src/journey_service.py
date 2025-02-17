# 
# Python FastAPI implentation for Pendo.JourneyService
# Author: Catherine Weightman
# Created: 13/02/2025
#

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def journey():
    return {"message": "Journey"}

@app.get("/view")
def journey():
    return {"message": "View Journey"}

@app.post("/create/")
def create_journey():
    item = "Create Journey"
    return item