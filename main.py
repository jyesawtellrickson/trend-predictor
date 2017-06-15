"""
pseudocode

# crawlers extract discussions/tweets, ~1000 / month.
# save these to a file in format (date, weight, string)
# weight is calculated as the number of responses / upvotes / retweets
reddit_crawleri # title of discussion
twitter_crawler # tweet
forum_crawler # title of post

# prepare data
for crawled_doc:
    clean (remove links, irrelevant discussions)
    calculate parts of speech pos # improve lemmatization
    lemmatize
    remove stop words # could do with cleaning?

# create time series
divide into monthly buckets
combine docs
calculate frequency distributions
generate monthly figures for each n-grams, take top 10
add in google_trends data for each term (is it being searched more?)
normalise with total number of mentions / month # 0 values where no data found

# detect increases
apply a smoothing filter
use a threshold to flag terms that are increasing - Dickey-Fuller test
plot graphs for these terms and further inspect behaviour

# perform sanity check - are students talking about this?
for term in flagged_terms:
    check student posts on twitter

"""
from reddit_crawler import RedditCrawler
from twitter_crawler import TwitterCrawler
from trend_analyser import TrendAnalyser
from credentials import *

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

# Analyse Data
trendy = TrendAnalyser()
trendy.load_source('reddit')
trendy.create_time_series()
trendy.stats_tests()

