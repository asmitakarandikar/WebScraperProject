from Scrape import Scrape
import json

elements_to_scrape = {}

f = open("scrape.json")
data = f.read()
f.close()
elements_to_scrape = json.loads(data)

s = Scrape("TSLA", elements_to_scrape)
print(s.summary())