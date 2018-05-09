import tweepy
import os
import csv
import math
import urllib
from pymongo import MongoClient

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
    return urllib.quote_plus(q)

def formGeocodeString(lat, lng, rad, unit):
    return str(lat) + ',' + str(lng) + ',' + str(rad) + unit

def getCount(api, q, terms, geocode, tweetsSeen):
    results = tweepy.Cursor(api.search, q=q, count=100, geocode=geocode).items(1000)
    count = 0
    for tweet in results:
        tweetFound = tweetsSeen.find_one({'_id': tweet.id})
        if tweetFound is not None:
            continue

        for term in terms:
            if term.lower() in tweet.text.lower():
                document = {'_id': tweet.id}
                tweetsSeen.insert_one(document)
                count += 1
                break
                #print(count)
                #print(tweet.text)
                #print(" ")
    return count

def setupAPI():
    auth = tweepy.OAuthHandler(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'))
    auth.set_access_token(os.environ.get('TWITTER_API_ACCESS_TOKEN'), os.environ.get('TWITTER_API_ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def row2TweetCount(api, row, q, terms, tweetsSeen):
    area_sq_m = int(row[1])
    lat = float(row[2])
    lng = float(row[3])
    area_sq_km = float(area_sq_m) / 1000000
    rad_km = (area_sq_km/math.pi) ** 0.5 #assume a circular area
    if rad_km < 1:
        rad_km = 1
    else:
        rad_km = int(rad_km)
    geocode = formGeocodeString(lat, lng, rad_km, 'km')
    count = getCount(api, q, terms, geocode, tweetsSeen)
    return (count, rad_km, lat, lng)

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


mongoUri = 'mongodb://' + os.environ.get('DATABASE_USERNAME') + ':' + \
    os.environ.get('DATABASE_PASSWORD') + '@ds217360.mlab.com:17360/sightlines'
client = MongoClient(mongoUri)
db = client['sightlines']
result = db['washington']
tweetsSeen = db['tweetsSeen']

api = setupAPI()
terms = getTerms('top_40_instagram_workout.csv')
q = terms2Query(terms)

with open('../state_census_tracts/Washington_state_results.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(reader):
        if i==0:#<158
            continue
        code = row[0]
        match = result.find_one({'_id': code})
        if match is not None:
            print(i)
            print("")
            continue
        count, rad_km, lat, lng = row2TweetCount(api, row, q, terms, tweetsSeen)
        print(i)
        print(code)
        print(count)
        print("")
        document = {'_id': code, 'rad_km': rad_km, 'latitude': lat , 'longitude': lng, 'count': count}
        result.insert_one(document)
