#from pymongo import MongoClient
import tweepy
import os
import csv
import math

def hashtags2Query(hashtags):
    q = ''
    for i, hashtag in enumerate(hashtags):
        if i < len(hashtags) - 1:
            q += (hashtag + ' OR ')
        else:
            q += hashtag
    return q

def formGeocodeString(lat, lng, rad, unit):
    return str(lat) + ',' + str(lng) + ',' + str(rad) + unit

def getCount(api, hashtags, geocode, items):
    #print(geocode)
    q = hashtags2Query(hashtags)
    results = tweepy.Cursor(api.search, q=q, count=100, geocode=geocode).items(items)
    count = 0
    for tweet in results:
        #print(tweet)
        for hashtag in hashtags:
            if hashtag.lower() in tweet.text.lower():
                count += 1
                #print(count)
                #print(tweet.text)
                #print(" ")
                break
    return count

def setupAPI():
    auth = tweepy.OAuthHandler(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'))
    auth.set_access_token(os.environ.get('TWITTER_API_ACCESS_TOKEN'), os.environ.get('TWITTER_API_ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def row2TweetCount(row, api, hashtags):
    code = row[0]
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
    return getCount(api, hashtags, geocode, 1000)

api = setupAPI()
hashtags = ['#Cardio', '#Cycling', '#FitFam', '#FitLife', '#Fitness', '#FitnessAddict', '#Sweat', '#Weights', '#WeightTraining', '#Workout']
with open('San_Bernardino_results.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(reader):
        if i==0:
            continue
        else:
            count = row2TweetCount(row, api, hashtags)
            #write this to a file
