from datetime import datetime

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from nltk.stem.porter import *

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import operator

from util import *


# should preprocess the text lemmatize/stem

def stem_doc(doc):
    stemmer = PorterStemmer()
    # split doc into words
    words = doc.split(' ')
    words = [stemmer.stem(word) for word in words]
    return ' '.join(words)


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


def generate_wordcloud(doc):
    wordcloud = WordCloud().generate(doc)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    return


def year_from_date(date_string):
    return datetime.strptime(date_string, '%a %b %d %H:%M:%S %z %Y').year


def plot_historical(historical_data):
    """
    Take historical data as dict of terms and plot a graph

    Args:
        historical_data:

    Returns:

    """
    for term in historical_data.keys():
        plt.plot([t[0] for t in historical_data[term]], [t[1] for t in historical_data[term]], label=term)
    plt.legend()
    plt.show()
    return


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


def create_counts(doc):
    """
    Create a frequency distribution from a list of tweets.

    Args:
        doc: list of tweets

    Returns: dict containing counts of top 100 words

    """
    cv = CountVectorizer(stop_words='english', max_features=100)
    X = cv.fit_transform(doc)
    freq = np.ravel(X.sum(axis=0))
    vocab = [v[0] for v in sorted(cv.vocabulary_.items(), key=operator.itemgetter(1))]
    fdist = dict(zip(vocab, freq))
    return fdist


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


analyse_tweets()
# done


