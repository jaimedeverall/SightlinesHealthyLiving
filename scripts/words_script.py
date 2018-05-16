import tweepy
import os
import csv
import math
import urllib
import pickle

def terms2Query(terms):
    q = ''
    for i, term in enumerate(terms):
        if i < len(terms) - 1:
            q += (term + ' OR ')
        else:
            q += term
    return urllib.quote_plus(q)

def getTweets(api, q, terms, usersSeen, tweetsSeen, term2Count):
    results = tweepy.Cursor(api.search, q=q, count=100).items(2000)
    count = 0
    for tweet in results:
        atLeastOneTermFound = False
        for term in terms:
            if term.lower() in tweet.text.lower():
                atLeastOneTermFound = True
                break
        if atLeastOneTermFound == False:
            continue

        user_id = tweet.user.id
        tweet_id = tweet.id
        if tweet_id not in tweetsSeen and user_id not in usersSeen:
            print count
            tweetsSeen.append(tweet_id)
            usersSeen.append(user_id)
            tweet_text = tweet.text
            for word in tweet_text.split():
                #if not word.startswith("#"):
                term = word.lower()
                if term in term2Count:
                    term2Count[term] += 1
                else:
                    term2Count[term] = 1
            count += 1
    return sorted( ((v,k) for k,v in term2Count.iteritems()), reverse=True)


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

#20,000
usersSeen = pickle.load( open( "usersSeen.p", "rb") )
tweetsSeen = pickle.load( open( "tweetsSeen.p", "rb") )
term2Count = pickle.load( open( "term2Count.p", "rb") )

results = getTweets(api, q, terms, usersSeen, tweetsSeen, term2Count)

pickle.dump( usersSeen, open( "usersSeen.p", "wb" ) )
pickle.dump( tweetsSeen, open( "tweetsSeen.p", "wb" ) )
pickle.dump( term2Count, open( "term2Count.p", "wb" ) )

for row in results:
    num = int(row[0])
    if num >= 200:
        print(row[0])
        print(row[1])
        print("")
