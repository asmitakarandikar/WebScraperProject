from Scrape import Scrape
import json
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from requests import HTTPError, TooManyRedirects

app = FastAPI()

@app.get("/root")
def root():
    return "Hello World!"

elements_to_scrape = {}

f = open("scrape.json")
data = f.read()
f.close()
elements_to_scrape = json.loads(data)

s = Scrape("TSLA", elements_to_scrape)
print(s.summary())

@app.get("/v1/{symbol}/summary/")
def summary(symbol):
    summary_data = {}
    try:
        s = Scrape(symbol, elements_to_scrape)
        summary_data = s.summary()
        
    except TooManyRedirects:
        raise HTTPException(status_code=404, detail="{symbol} doesn't exist or cannot be found.")
    except HTTPError:
        raise HTTPException(status_code=500, detail="An error has occurred while processing the request.")

    return summary_data

@app.on_event("startup")
def startup():
    f = open("scrape.json")
    data = f.read()
    f.close()
    global elements_to_scrape
    elements_to_scrape = json.loads(data)