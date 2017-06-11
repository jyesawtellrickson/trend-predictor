import tweepy
from tweepy import OAuthHandler

from collections import Counter

from wordcloud import WordCloud
import matplotlib.pyplot as plt

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



# get tweets on the education hashtag
# count the number of times each user has tweeted on that hashtag
# get the tweets of the most common user, update score table with rt's and tags
# potentially also get following / friends from our top users to grow our education
# influencers
# continue getting tweets

"""
functions required:
    - get tweets for hashtag
    - count users, hashtags and tags
    - find most common user
"""

def tweets_for_user(api, username):
    number = 100
    # check username is string
    tweets = []
    user = api.get_user(username)
    for status in tweepy.Cursor(api.user_timeline, id=user.id).items(number):
        tweets += [status._json]
    # check the user is legit before returning
    # are they really a thought leader? or jobs
    test_edu = 0
    test = 0
    for tweet in tweets:
        test += tweet.text.find('job') >= 0
        test_edu += tweet.text.find('educat') >= 0
    test = test / len(tweets)
    # do they talk about education enough?
    if test > 0.5 or test_edu < 0.1:
        return
    return tweets


# need to add the use of since_id
def tweets_for_search(api, search, number):
    if not number:
        number = 150
    tweets = []
    # return results up to number
    for status in tweepy.Cursor(api.search, q=search).items(number):
        tweets += [status._json]
    return tweets

def tweets_to_text_date(tweets):
    return [(t['created_at'], t['text']) for t in tweets]


def remove_links(tweet_text):
    return tweet_text


def generate_wordcloud(doc):
    wordcloud = WordCloud().generate(doc)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    return


def get_tweets():
    HISTORICAL_TWEETS = tweets_for_search(api, "#education", 1500)
    # print([t.text for t in HISTORICAL_TWEETS])
    # get a count of user strings
    users = dict(Counter([t['user']['id_str'] for t in HISTORICAL_TWEETS]))

    top_10 = sorted(users, key=users.get, reverse=True)[:20]

    for user_id_str in top_10:
        print('getting tweets for user '+user_id_str)
        new_tweets = tweets_for_user(api, user_id_str)
        HISTORICAL_TWEETS += new_tweets

    output_file = open('historical_tweets.pkl', 'wb')

    pickle.dump(HISTORICAL_TWEETS, output_file)

    output_file.close()

def analyse_tweets():
    tweets_file = open('historical_tweets.pkl','rb')
    tweets = pickle.load(tweets_file)
    tweets_dt = tweets_to_text_date(tweets)
    # create old and new doc
    doc = " ".join([str(i[1]) for i in tweets_dt])
    # need to filter out bad tweets
    # ones containing careers, jobs, hiring
    stop_words = ['career', 'job', 'hire', 'hiring','https','t.co',
                  'Job','Hiring','Career', 'latest opening','recommend anyone','RT']
    for word in stop_words:
        doc = doc.replace(word, "")
    print(doc)
    generate_wordcloud(doc)



analyse_tweets()