import tweepy
from tweepy import OAuthHandler

from collections import Counter
from datetime import datetime

from util import *
from credentials import *

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

HISTORICAL_TWEETS = []

# get tweets on the education hashtag
# count the number of times each user has tweeted on that hashtag
# get the tweets of the most common user, update score table with rt's and tags
# potentially also get following / friends from our top users to grow our education
# influencers
# continue getting tweets
# should preprocess the text lemmatize/stem

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
    # check bio as well, does it have our keywords?
    test_edu = 0
    test = 0
    for tweet in tweets:
        test += tweet['text'].find('job') >= 0
        test_edu += tweet['text'].find('educat') >= 0
    test = test / len(tweets)
    # do they talk about education enough?
    # are they posting too often?
    if test > 0.5 or test_edu < 0.1:
        return
    return tweets

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except: # tweepy.RateLimitError:
            print("hit rate limit")
            break


# need to add the use of since_id
def tweets_for_search(api, search, number):
    if not number:
        number = 150
    tweets = []
    # return results up to number
    for status in limit_handled(tweepy.Cursor(api.search, q=search).items()):
        tweets += [status._json]
        # print updates to screen
        if len(tweets) % 100 == 0:
            print("{0} tweets processed".format(len(tweets)))
            save_file(tweets, "during_processing.pkl")
    return tweets


def update_tweeter_scores(tweets, scores):
    """
    take tweets and add to the user scores
    to help identify trend setters
    """
    for tweet in tweets:
        # one score for each tweet
        scores[tweet['user']['id_str']] += 1
        # one score for each mention
    return scores


def tweets_to_text_date(tweets):
    return [(t['created_at'], t['text']) for t in tweets]


def remove_links(tweet_text):
    return tweet_text


def year_from_date(date_string):
    return datetime.strptime(date_string, '%a %b %d %H:%M:%S %z %Y').year


def history_generator(tweets):
    """
    Create a dict of terms with frequency
    per month/year.

    Returns: dictionary containing terms with tuples of counts / year

    """
    # convert tweets to date and time
    tweets_td = tweets_to_text_date(tweets)
    start_year = 2010
    end_year = 2017
    counts_all = {}
    for year in range(start_year, end_year+1):
        process_tweets = [t[1] for t in tweets_td if year_from_date(t[0]) == year]
        if process_tweets != []:
            counts = create_counts(process_tweets)
            for term in counts:
                if term in counts_all.keys():
                    counts_all[term] += [(year, counts[term])]
                else:
                    counts_all[term] = [(year, counts[term])]
    return counts_all


def get_user_tweets(HISTORICAL_TWEETS):
    # get a count of user strings
    users = dict(Counter([t['user']['id_str'] for t in HISTORICAL_TWEETS]))
    top_10 = sorted(users, key=users.get, reverse=True)[:20]

    for user_id_str in top_10:
        print('getting tweets for user '+user_id_str)
        new_tweets = tweets_for_user(api, user_id_str)
        HISTORICAL_TWEETS += new_tweets

    return HISTORICAL_TWEETS


def generate_tweets_file():
    print("getting tweets for search term")
    tweets = tweets_for_search(api, "#education #teaching", None)
    save_file(tweets, 'historical_tweets_2.pkl')
    return


def analyse_tweets():
    tweets = load_file('during_processing.pkl')
    plot_historical(history_generator(tweets))
    # create old and new doc
    doc = " ".join([t['text'] for t in tweets])
    doc = stem_doc(doc)
    # need to filter out bad tweets
    # ones containing careers, jobs, hiring
    stop_words = ['career', 'job', 'hire', 'hiring','https','t.co', 'teach', 'educ',
                  'Job','Hiring','Career', 'latest opening','recommend anyone','RT']
    for word in stop_words:
        doc = doc.replace(word, "")
    generate_wordcloud(doc)


# generate_tweets_file()
analyse_tweets()
# done


