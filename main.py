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



############################################
could we train a model to predict the popularity of a post on reddit
then build our own titles based on twitter data?
NO - the whole point is that this is a changing time series and
the linguistic models can't do this sort of forward thinking.
"""
