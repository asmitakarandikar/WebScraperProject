from Scrape import Scrape
import json
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from requests import HTTPError, TooManyRedirects

app = FastAPI()

@app.get("/root")
def root():
    return "Hello World!"


s = Scrape("TSLA")
print(s.summary())

@app.get("/v1/{symbol}/summary/")
def summary(symbol):
    summary_data = {}
    try:
        s = Scrape(symbol)
        summary_data = s.summary()
        
    except TooManyRedirects:
        raise HTTPException(status_code=404, detail="{symbol} doesn't exist or cannot be found.")
    except HTTPError:
        raise HTTPException(status_code=500, detail="An error has occurred while processing the request.")

    return summary_data

@app.on_event("startup")
def startup():
    return 1
