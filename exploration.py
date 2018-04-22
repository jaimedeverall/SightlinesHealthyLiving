#https://twitter.com/search?l=&q=%23excercise%20near%3A%22Stanford%2C%20CA%22%20within%3A15mi&src=typd

#https://api.twitter.com/1.1/search/tweets.json?l=&q=%23excercise%20near%3A%22Stanford%2C%20CA%22%20within%3A15mi&src=typd

import tweepy
import os
import geopy
from geopy.geocoders import Nominatim


auth = tweepy.OAuthHandler(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'))
auth.set_access_token(os.environ.get('TWITTER_API_ACCESS_TOKEN'), os.environ.get('TWITTER_API_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)

q = '#Cardio OR #Cycling OR #Elliptical OR #FitFam OR #FitLife OR #Fitness OR #FitnessAddict OR #GetOutside OR #GetStrong OR #GirlsWhoLift OR #GymLife OR #GymTime OR #NoPainNoGain OR #PersonalTrainer OR #Sweat OR #Treadmill OR #Weights OR #WeightTraining OR #Workout'

geolocator = Nominatim()
location = geolocator.geocode("30301")
geocode_str = str(location.latitude) + ',' + str(location.longitude) + ',15mi'
#37.4262942886,-122.157360145,15mi for zip code 94305

print(geocode_str)

results = api.search(q, since_id=1, geocode=geocode_str)

print(len(results))

for tweet in results:
  print tweet

#for tweet in public_tweets:
#     print tweet.text