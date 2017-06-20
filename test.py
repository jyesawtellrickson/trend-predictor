"""
Test showing basic usage of the models.
"""

from reddit_crawler import RedditCrawler
from twitter_crawler import TwitterCrawler
from trend_analyser import TrendAnalyser
from credentials import *

"""
# collect reddit data
reddit_crawler = RedditCrawler(['education'], ['2015', '2016'])
reddit_crawler.authenticate(reddit_client_id, reddit_secret)
reddit_crawler.get_submissions()
reddit_crawler.prepare_snippets()

# collect twitter data
twitter_crawler = TwitterCrawler(['#education'], ['2015', '2016'])
twitter_crawler.authenticate(consumer_key, consumer_secret, access_token, access_secret)
twitter_crawler.get_tweets()
twitter_crawler.prepare_snippets()
"""
# Analyse Data
trendy = TrendAnalyser()
# trendy.load_source('reddit')
# trendy.create_time_series()
trendy.stats_tests()

