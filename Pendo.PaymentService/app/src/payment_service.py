from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/take")
def take():
    return {"Hello" : "World"}

def some_testing_function(param):
    return param