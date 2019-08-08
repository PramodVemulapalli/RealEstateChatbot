# Module: f2.py
from bs4 import BeautifulSoup

import urllib.parse
import requests
import json
import lxml
import sys
import os
import random

def get_headers():
    # Creating headers.
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, sdch, br',
               'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
               'cache-control': 'max-age=0',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    return headers


def get_reqheaders():
    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    return req_headers


def getlatlngs(zippy):
    geocodeurl = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + str(zippy) + '&key=' + os.environ['GOOGLEMAPSAPIKEY']
    geocoderesp = requests.get(geocodeurl)
    geocodejson = geocoderesp.json()
    geocode_jsonstr = json.dumps(geocodejson)
    resp = json.loads(geocode_jsonstr)
    nelat=resp['results'][0]['geometry']['bounds']['northeast']['lat']
    nelng=resp['results'][0]['geometry']['bounds']['northeast']['lng']
    swlat=resp['results'][0]['geometry']['bounds']['southwest']['lat']
    swlng=resp['results'][0]['geometry']['bounds']['southwest']['lng']

    return nelat, nelng, swlat, swlng


def geturlinfo(zippy, minprice, maxprice, nelat, nelng, swlat, swlng):
    url_base = 'https://www.zillow.com/austin-tx-' + str(zippy)+ '/houses/3-_beds/?searchQueryState='
    url_data = """
    {
    "pagination":{},
    "mapBounds":{"west":"""+ str(swlng) + ',"east":'+ str(nelng) +',"south":'+str(swlat)+',"north":'+str(nelat)+'}' + """,
    "usersSearchTerm":"""+str(zippy)+""",
    "regionSelection":[{"regionId":92615,"regionType":7}],
    "isMapVisible":true,
    "mapZoom":14,
    "filterState":{"price":{"min":""" + str(minprice) + ',"max":' + str(maxprice) + '},' + """
    "monthlyPayment":{"min":2209,"max":2946},
    "beds":{"min":3},
    "sqft":{"min":0,"max":2000},
    "isAuction":{"value":false},
    "isCondo":{"value":false},
    "isManufactured":{"value":false},
    "isLotLand":{"value":false},
    "isTownhouse":{"value":false}},
    "isListVisible":true
    }"""

    return url_base, url_data

def get_url(zipcode, upperlimit):
    # Creating Zillow URL based on the filter.

    req_headers = get_reqheaders()
    zippy = int(zipcode)
    nelat, nelng, swlat, swlng = getlatlngs(zippy)
    minprice = 200000
    maxprice = int(upperlimit)
    with requests.Session() as s:
        url_base, url_data = geturlinfo(zippy, minprice, maxprice, nelat, nelng, swlat, swlng)
        r = s.get(url_base+urllib.parse.quote(url_data), headers=req_headers)
        soup = BeautifulSoup(r.content, 'lxml')
        prices = soup.findAll('article', {'class': 'list-card'})
    lenofprices = len(prices)-1
    randhome = random.randint(0,lenofprices)
    return prices[randhome].find('a', {'class': 'list-card-link'})['href'], prices[randhome].find('img')['src']



# Example 2: class methods to store and retrieve properties
class fromtheweb(object):
    def __init__(self):
        self.zipcode = 75039
        self.upperLimit = 200000
    def setzipcode(self, myVar):
        self.zipcode = myVar
    def setupperLimit(self, myVar):
        self.upperLimit = myVar
    def getresult(self):
        return get_url(self.zipcode , self.upperLimit)
