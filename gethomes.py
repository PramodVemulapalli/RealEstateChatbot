# Module: f2.py
from bs4 import BeautifulSoup

import urllib.parse
import requests
import json
import lxml
import sys
import os
import random
import pdb

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


def geturlinfo(zippy, minprice, maxprice, bedrooms, nelat, nelng, swlat, swlng):
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
    "beds":{"min":""" + str(bedrooms) + """},
    "sqft":{"min":0,"max":2000},
    "isAuction":{"value":false},
    "isCondo":{"value":false},
    "isManufactured":{"value":false},
    "isLotLand":{"value":false},
    "isTownhouse":{"value":false}},
    "isListVisible":true
    }"""

    return url_base, url_data

def get_home(zipcode, upperlimit, bedrooms):
    # Creating Zillow URL based on the filter.
    rand_home = -1
    req_headers = get_reqheaders()
    zippy = int(zipcode)
    nelat, nelng, swlat, swlng = getlatlngs(zippy)
    minprice = 200000
    maxprice = int(upperlimit)
    with requests.Session() as s:
        url_base, url_data = geturlinfo(zippy, minprice, maxprice, bedrooms, nelat, nelng, swlat, swlng)
        r = s.get(url_base+urllib.parse.quote(url_data), headers=req_headers)
        soup = BeautifulSoup(r.content, 'lxml')
        prices = soup.findAll('article', {'class': 'list-card'})
    lenofprices = len(prices)-1
    print('len of prices = ' + str(lenofprices), file=sys.stdout)
    randhome = random.randint(0,lenofprices)
    ahome = prices[randhome]
    return ahome


def get_url(zipcode, upperlimit, bedrooms):

    ahome = get_home(zipcode, upperlimit, bedrooms)
    return ahome.find('a', {'class': 'list-card-link'})['href'], ahome.find('img')['src']



def get_homeinfo(homedata, checkstring):
    checkflag=0;
    for data in homedata:
        if (checkflag == 1):
            return data.text
        if (data.text == checkstring):
            checkflag = 1
    return ''


def get_homeanswer(homedata, replyquestion):

    if replyquestion == "bedrooms" :
        homeinfo = get_homeinfo(homedata, 'Bedrooms')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " bedrooms"
    elif replyquestion == "bathrooms" :
        homeinfo = get_homeinfo(homedata, 'Bathrooms')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " bathrooms"
    elif replyquestion == "flooring" :
        homeinfo = get_homeinfo(homedata, 'Flooring')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " flooring"
    elif replyquestion == "heating" :
        homeinfo = get_homeinfo(homedata, 'Heating features')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " heating"
    elif replyquestion == "appliances" :
        homeinfo = get_homeinfo(homedata, 'Appliances included in sale')
        if (homeinfo != ''):
            return "According to our information, " + str(homeinfo) + " are the appliances that are included in the sale"
    elif replyquestion == "area" :
        homeinfo = get_homeinfo(homedata, 'Total interior livable area')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " of total interior livable area"
    elif replyquestion == "parking" :
        homeinfo = get_homeinfo(homedata, 'Parking features')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " for parking"
    elif replyquestion == "garage" :
        homeinfo = get_homeinfo(homedata, 'Garage spaces')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " garage spaces"
    elif replyquestion == "stories" :
        homeinfo = get_homeinfo(homedata, 'Stories')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " stories"
    elif replyquestion == "exterior" :
        homeinfo = get_homeinfo(homedata, 'Exterior features')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " exterior"
    elif replyquestion == "fencing" :
        homeinfo = get_homeinfo(homedata, 'Fencing')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " fencing"
    elif replyquestion == "lot" :
        homeinfo = get_homeinfo(homedata, 'Lot size')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " in terms of lot size"
    elif replyquestion == "foundation" :
        homeinfo = get_homeinfo(homedata, 'Foundation')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " foundation"
    elif replyquestion == "roof" :
        homeinfo = get_homeinfo(homedata, 'Roof')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " type of roof"
    elif replyquestion == "year" :
        homeinfo = get_homeinfo(homedata, 'Year built')
        if (homeinfo != ''):
            return "According to our information, the home was built in " + str(homeinfo)
    elif replyquestion == "utilities" :
        homeinfo = get_homeinfo(homedata, 'Utilities for property')
        if (homeinfo != ''):
            return "According to our information, the home has " + str(homeinfo) + " utilities"
    elif replyquestion == "pets" :
        homeinfo = get_homeinfo(homedata, 'Pets allowed')
        if (homeinfo != ''):
            return "Does the home allow pets ? " + str(homeinfo)
    elif replyquestion == "HOA" :
        homeinfo = get_homeinfo(homedata, 'HOA fee')
        if (homeinfo != ''):
            return "Does the home have a HOA fee ? " + str(homeinfo)
    elif replyquestion == "tax" :
        homeinfo = get_homeinfo(homedata, 'Annual tax amount')
        if (homeinfo != ''):
            return "According to our information, the annual tax amount for the home is  " + str(homeinfo)
    elif replyquestion == "architecture" :
        homeinfo = get_homeinfo(homedata, 'Architectural style')
        if (homeinfo != ''):
            return "According to our information, the architectural style of the home is " + str(homeinfo)
    elif replyquestion == "county" :
        homeinfo = get_homeinfo(homedata, 'County Or Parish')
        if (homeinfo != ''):
            return "According to our information, the home is in " + str(homeinfo) + " county"
    elif replyquestion == "value" :
        homeinfo = get_homeinfo(homedata, 'Tax assessed value')
        if (homeinfo != ''):
            return "According to our information, the home's tax assessed value is " + str(homeinfo)
    elif replyquestion == "possession" :
        homeinfo = get_homeinfo(homedata, 'Posession')
        if (homeinfo != ''):
            return "According to our information, the home has the possession type of " + str(homeinfo)
    elif replyquestion == "country" :
        homeinfo = get_homeinfo(homedata, 'Country')
        if (homeinfo != ''):
            return "According to our information, the home is in " + str(homeinfo)
    else:
        return "Sorry. We donot have any information about this in our records"

    return "Sorry. We donot have any information about this in our records"

def get_reply(zipcode, upperlimit, bedrooms, homeurl, replyquestion):

    #ahome, randhome = get_home(zipcode, upperlimit, bedrooms, homeindex)
    #ahomeurl = ahome.find('a', {'class': 'list-card-link'})['href']
    with requests.Session() as s:
        r2 = s.get(homeurl, headers=get_reqheaders())
    soup2 = BeautifulSoup(r2.content, 'lxml')
    homedata = soup2.findAll('td')
    return get_homeanswer(homedata, replyquestion)

# Example 2: class methods to store and retrieve properties
class fromtheweb(object):
    def __init__(self):
        self.zipcode = 75039
        self.upperLimit = 200000
        self.bedrooms = 1
    def setzipcode(self, myVar):
        self.zipcode = int(myVar)
    def setupperLimit(self, myVar):
        self.upperLimit = int(myVar)
    def setbedrooms(self, myVar):
        self.bedrooms = int(myVar)
    def sethomeurl(self, myVar):
        self.homeurl = str(myVar)
    def getresult(self):
        return get_url(self.zipcode , self.upperLimit, self.bedrooms)
    def getreply(self, replyquestion):
        return get_reply(self.zipcode , self.upperLimit, self.bedrooms, self.homeurl, replyquestion)
