import tweepy
from tweepy import OAuthHandler

from collections import Counter
from datetime import datetime

from util import *


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


class TwitterCrawler:

    def __init__(self, queries, dates, twitter_file='twitter_file.pkl', snippet_file='twitter_snippet_file.pkl'):
        # initialise basic props
        self.twitter = None
        self.queries = queries
        self.dates = dates
        self.twitter_file = twitter_file
        self.snippet_file = snippet_file

    def authenticate(self, consumer_key, consumer_secret, access_token, access_secret):
        """
        Authenticate the twitter API and prepare for processing.
        Args:
            consumer_key:
            consumer_secret:
            access_token:
            access_secret:

        Returns:

        """
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        try:
            self.twitter = tweepy.API(auth)
            print("Successfully authenticated")
        except:
            print("Failed to authenticate")
        return

    def get_tweets(self):
        """
        Gathers the tweets for the provided queries.
        Returns:

        """
        print("Getting tweets for search terms")
        tweets = []
        for query in self.queries:
            # return results up to number
            for status in self.limit_handled(tweepy.Cursor(self.twitter.search, q=query).items()):
                tweets += [status._json]
                # print updates to screen
                if len(tweets) % 100 == 0:
                    print("{0} tweets processed".format(len(tweets)))
                    save_file(tweets, self.twitter_file)
        save_file(tweets, self.twitter_file)
        return

    @staticmethod
    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except:  # tweepy.RateLimitError:
                print("hit rate limit")
                break

    def tweets_for_user(self, username):
        number = 100
        # check username is string
        tweets = []
        # get user id from username
        user = self.twitter.get_user(username)
        for status in tweepy.Cursor(self.twitter.user_timeline, id=user.id).items(number):
            tweets += [status._json]
        # check the user is legit before returning
        if self.test_user(tweets):
            return tweets
        return None

    @staticmethod
    def test_user(tweets):
        # are they really a thought leader? or jobs
        # check bio as well, does it have our keywords?
        test_edu = 0
        test_jobs = 0
        for tweet in tweets:
            test_jobs += tweet['text'].find('job') >= 0
            test_edu += tweet['text'].find('educat') >= 0
        test_jobs /= len(tweets)
        test_edu /= len(tweets)
        # do they talk about education enough?
        # are they posting too often?
        if test_jobs > 0.5 or test_edu < 0.1:
            return False
        return True

    @staticmethod
    def remove_links(tweet_text):
        return tweet_text

    @staticmethod
    def year_from_date(date_string):
        return datetime.strptime(date_string, '%a %b %d %H:%M:%S %z %Y').year

    @staticmethod
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

    @staticmethod
    def expand_top_tweeters(tweets, user_count=20):
        # get a count of user strings
        users = dict(Counter([t['user']['id_str'] for t in tweets]))
        top_users = sorted(users, key=users.get, reverse=True)[:user_count]

        for user_id_str in top_users:
            print('getting tweets for user '+user_id_str)
            new_tweets = tweets_for_user(api, user_id_str)
            tweets += new_tweets
        return tweets

    def prepare_snippets(self):
        tweets = load_file(self.twitter_file)
        snippets = [(t['created_at'], t['text'], 1) for t in tweets]
        save_file(snippets, self.snippet_file)
        return



