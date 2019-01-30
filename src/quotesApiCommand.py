
import requests
from pprint import pprint
import json
import random
def getQuotes():
    r = requests.get('https://quotesapi.sbdev.nl/quote/all')
    if(r.status_code == 200):
        return json.loads(r.text)

    else:
        return None

def createQuote(quote, author):
    r = requests.post('https://quotesapi.sbdev.nl/quote/create',{
        'quote': quote,
        'author': author
    })
    return r.status_code


def randomQuote():
    r = requests.get('https://quotesapi.sbdev.nl/quote/find')
    if(r.status_code == 200):
        return json.loads(r.text)

def getQuote():
    r = requests.get('https://quotesapi.sbdev.nl/quote/find/' + 1)
    print(r.text)    

if __name__ == "__main__":
    # testQuote = createQuote("Test", "Sascha achter zijn computer")
    # if(testQuote == 200):
    #     print("Quote toegevoegd")

    getQuote()