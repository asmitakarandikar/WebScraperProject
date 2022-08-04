import requests
from bs4 import BeautifulSoup
import json
class Scrape():

    def __init__(self, symbol):
        
        self.__summary ={}

        url_list = []
        url_list.append(["https://finance.yahoo.com/quote/" + symbol,"ScrapeYahoo.json"])
        url_list.append(["https://www.marketwatch.com/investing/stock/" + symbol, "ScrapeMW.json"])
        url_list.append(["https://www.google.com/finance/quote/" + symbol + ":NASDAQ", "ScrapeGoog.json"])
        siteList = ["Yahoo", "MarketWatch", "Google"]
        count =0
        for url in url_list:
            elements_to_scrape = {}
            f = open(url[1])
            data = f.read()
            f.close()
            elements_to_scrape = json.loads(data)
            
            r = requests.get(url[0])
            if(r.url != url[0]): # redirect occurred; likely symbol doesn't exist or cannot be found.
                raise requests.TooManyRedirects()

            r.raise_for_status()
            
            self.soup = BeautifulSoup(r.text, "html.parser")

            entry= {}

            for el in elements_to_scrape["elements"]:
                tag = self.soup.select_one(el["from"])
                if tag != None:
                    entry[el["to"]] = tag.get_text()
            self.__summary[siteList[count]] = entry
            count +=1

    def summary(self):
        return self.__summary