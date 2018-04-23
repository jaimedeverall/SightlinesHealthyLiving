import tweepy
import os
import csv

def zip2LatLng(zipcode):
    with open('zipcodes.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i==0:
                continue
            zip = row[0].strip('"')
            if zip == zipcode:
                return (float(row[5]), float(row[6]))
    return (None, None)

def hashtags2Query(hashtags):
    q = ''
    for i, hashtag in enumerate(hashtags):
        if i < len(hashtags) - 1:
            q += (hashtag + ' OR ')
        else:
            q += hashtag
    return q

auth = tweepy.OAuthHandler(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'))
auth.set_access_token(os.environ.get('TWITTER_API_ACCESS_TOKEN'), os.environ.get('TWITTER_API_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth, wait_on_rate_limit=True)

hashtags = ['#Cardio', '#Cycling', '#FitFam', '#FitLife', '#Fitness', '#FitnessAddict', '#Sweat', '#Weights', '#WeightTraining', '#Workout']

q = hashtags2Query(hashtags)

lat, lng = zip2LatLng('10002')

geocode_str = str(lat) + ',' + str(lng) + ',10mi'

#30301
#48205
#10012
#10025
#10002

print(geocode_str)

#results = api.search(q, geocode=geocode_str, rpp=100)

results = tweepy.Cursor(api.search, q=q, count=100, geocode=geocode_str).items(1000)

count = 0
for tweet in results:
  for hashtag in hashtags:
      if hashtag.lower() in tweet.text.lower():
          count += 1
          print(count)
          print(tweet.text)
          print(" ")
          break
