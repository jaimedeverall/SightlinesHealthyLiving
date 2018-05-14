import tweepy
import os
import csv
import math
import urllib

def terms2Query(terms):
    q = ''
    for i, term in enumerate(terms):
        if i < len(terms) - 1:
            q += (term + ' OR ')
        else:
            q += term
    return urllib.quote_plus(q)

def getTweets(api, q, terms):
    tweet_dict = {}
    results = tweepy.Cursor(api.search, q=q, count=100).items(5000)
    count = 0
    for tweet in results:
        print count
        tweet_text = tweet.text
        for word in tweet_text.split():
            if not word.startswith("#"):
                if word.lower() in tweet_dict:
                    tweet_dict[word.lower()] += 1
                else:
                    tweet_dict[word.lower()] = 1
        count += 1
    final_list = sorted( ((v,k) for k,v in tweet_dict.iteritems()), reverse=True)
    print final_list


def setupAPI():
    auth = tweepy.OAuthHandler(os.environ.get('TWITTER_API_KEY'), os.environ.get('TWITTER_API_SECRET'))
    auth.set_access_token(os.environ.get('TWITTER_API_ACCESS_TOKEN'), os.environ.get('TWITTER_API_ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

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


terms = getTerms('top_40_instagram_workout.csv')
q = terms2Query(terms)
api = setupAPI()
getTweets(api, q, terms)

