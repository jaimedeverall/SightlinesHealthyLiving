#from pymongo import MongoClient
import tweepy
import os
import csv
import math

def zip2LatLng(zipcode):
    with open('original_files/zipcodes.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i==0:
                continue
            zip = row[0].strip('"')
            if zip == zipcode:
                return (float(row[5]), float(row[6]))

def terms2Query(terms):
    q = ''
    for i, term in enumerate(terms):
        if i < len(terms) - 1:
            q += (term + ' OR ')
        else:
            q += term
    return q

def formGeocodeString(lat, lng, rad, unit):
    return str(lat) + ',' + str(lng) + ',' + str(rad) + unit

#Returns a tuple of total tweets found as well as total tweets that contain terms
def getCount(api, terms, geocode, items):
    q = terms2Query(terms)
    results = tweepy.Cursor(api.search, q=q, count=100, geocode=geocode).items(items)
    count = 0
    totalCount = 0
    for tweet in results:
        #print(tweet)
        totalCount += 1
        for term in terms:
            if term.lower() in tweet.text.lower():
                count += 1
                print(count)
                print(tweet.text)
                print(" ")
                break
    return (count, totalCount)

def setupAPI():
    auth = tweepy.OAuthHandler(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'))
    auth.set_access_token(os.environ.get('TWITTER_API_ACCESS_TOKEN'), os.environ.get('TWITTER_API_ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def row2TweetCount(row, api, terms):
    area_sq_m = int(row[1])
    lat = row[2]
    lng = row[3]
    area_sq_km = float(area_sq_m) / 1000000
    rad_km = (area_sq_km/math.pi) ** 0.5 #assume a circular area
    print(rad_km)
    if rad_km < 1:
        rad_km = 1
    else:
        rad_km = int(rad_km)
    geocode = formGeocodeString(lat, lng, rad_km, 'km')
    return getCount(api, terms, geocode, 1000)

#max of 500 characters (including operators)
def getTerms(file_name):
    with open('../terms/' + file_name, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        terms = []
        for i, row in enumerate(reader):
            term = row[0]
            if len(term) > 0:
                terms.append(term)
        return terms

api = setupAPI()
terms = getTerms('state_level_exercise.csv')
lat = 37.166111
lng = -119.449444
#Area = 121,697
geocode = formGeocodeString(lat, lng, 228, 'mi')
print(getCount(api, terms, geocode, 5000))
