import tweepy
from tweepy import OAuthHandler

import json
import pickle

consumer_key = "aTBKDuDix3ILWXdCSMC2rwoUV"
consumer_secret = "wBdoCAXY7lkL0QDBy5IsE6zbDk9BowJksMIKwafKn0JvWvkh4B"
access_token = "899746063-eTIFXfPAhbZiwIzJDDpFVdwP54IE2m2KDPsF2NMf"
access_secret = "vyp0wZY8H2uccAFE1I8dx6OuFAMAZCPPPuuY4A1mAt1bt"


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

HISTORICAL_TWEETS = []

def process_or_store(tweet, HISTORICAL_TWEETS):
    #print(json.dumps(tweet))
    HISTORICAL_TWEETS += [json.dumps(tweet)]
    return HISTORICAL_TWEETS


for tweet in tweepy.Cursor(api.user_timeline).items():
    HISTORICAL_TWEETS = process_or_store(tweet._json, HISTORICAL_TWEETS)
    print(tweet.text)

output_file = open('historical_tweets.pkl', 'wb')

pickle.dump(HISTORICAL_TWEETS, output_file)


# get tweets on the education hashtag
# count the number of times each user has tweeted on that hashtag
# get the tweets of the most common user, update score table with rt's and tags
# continue getting tweets

"""
functions required:
    - get tweets for hashtag
    - count users, hashtags and tags
    - find most common user
"""