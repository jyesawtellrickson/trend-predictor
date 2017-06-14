from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

import statsmodels.tsa.stattools as ts
from statsmodels.nonparametric.smoothers_lowess import lowess
from math import factorial
import numpy as np

import pandas as pd

from math import floor, ceil

from nltk.stem.porter import *

from collections import Counter

from datetime import datetime
from dateutil.relativedelta import *

from util import *


def stem_doc(doc):
    """
    Takes a doc and applies stemming to words.
    Args:
        doc: string

    Returns: stemmed doc string

    """
    stemmer = PorterStemmer()
    # split doc into words
    words = doc.split(' ')
    words = [stemmer.stem(word) for word in words]
    return doc #' '.join(words)


def generate_wordcloud(doc):
    """
    Given a doc, generate a wordcloud.
    Args:
        doc: string

    Returns:

    """
    wordcloud = WordCloud().generate(doc)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    return


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


def history_generator(doc):
    """
    Create a dict of terms with frequency
    per month/year.

    Returns: dictionary containing terms with tuples of counts / year

    """
    # convert tweets to date and time
    start_year = 2010
    end_year = 2017
    counts_all = {}
    for year in range(start_year, end_year+1):
        process_tweets = [t[1] for t in doc if t[0] == year]
        if process_tweets != []:
            counts = create_counts(process_tweets)
            for term in counts:
                if term in counts_all.keys():
                    counts_all[term] += [(year, counts[term])]
                else:
                    counts_all[term] = [(year, counts[term])]
    return counts_all


def snippets_to_doc(snippets):
    """
    Takes a list of snippets and returns a doc.
    Args:
        snippets: list of snippet

    Returns: doc as string

    """
    # multiply each by the weight
    # *int(s[2])
    return " ".join([s[1] for s in snippets])


def divide_monthly(docs):
    """
    Take a list of snippets and return dict of snippets
    divided into monthly bins.
    Args:
        docs: list of snippets

    Returns: dict containing snippets

    """
    # seperate out docs based on month
    dates = [d[0] for d in docs]
    min_date = datetime.fromtimestamp(min(dates)).replace(day=1).date()
    # should be the following month, really
    max_date = datetime.fromtimestamp(max(dates)).replace(day=1).date() + relativedelta(months=1)
    monthly_docs = {}
    while min_date <= max_date:
        min_date = min_date + relativedelta(months=1)
        monthly_docs[min_date] = [d for d in docs if datetime.fromtimestamp(d[0]).date() < min_date]
    return monthly_docs


def remove_stop_words(doc):
    """
    Remove stopwords from a doc
    Args:
        doc: string

    Returns: string

    """
    cached_stop_words = set(stopwords.words("english"))
    cached_stop_words.update(['education','&','-','--','2012','8','america','american'])
    doc = ' '.join([word for word in doc.split() if word.lower() not in cached_stop_words])
    return doc


def create_counts(doc, count=200):
    """
    Create a frequency distribution from a doc.

    Args:
        doc: string
        count: int number of terms to return

    Returns: dict containing counts of terms

    """
    """
    # if doc is very big, this breaks, split first
    if len(doc) > 5000:
        chunks = 10
    else:
        chunks = 1
    freqs = Counter()
    doc_length = 0
    for i in range(0, chunks):
        crb = floor(i*len(doc)/chunks)
        crt = floor((i+1)*len(doc)/chunks) - 1
        doc_chunk = doc[crb:crt].lower().split()
        doc_length += len(doc_chunk)
        tmp = Counter(doc_chunk)
        freqs.update(tmp)
    freqs = freqs.most_common(count)
    """
    print(len(doc))
    doc = doc[0:5000000]
    doc = doc.lower().split()
    freqs = dict(Counter(doc).most_common(count))
    # normalise
    for word in freqs.keys():
        freqs[word] = freqs[word] / len(doc)
    return freqs


def analyse_snippets():
    snippets = load_file('reddit_for_analysis.pkl')
    # divide monthly
    monthly_snippets = divide_monthly(snippets)
    df = pd.DataFrame()
    count = 0
    # convert to docs and stem
    for key in monthly_snippets.keys():
        monthly_snippets[key] = stem_doc(remove_stop_words(snippets_to_doc(monthly_snippets[key])))
        counts = create_counts(monthly_snippets[key])
        df_temp = pd.DataFrame([(key, c[0], c[1]) for c in list(counts.items())])
        df_temp = df_temp.pivot(index=1, columns=0, values=2)
        df = pd.concat([df, df_temp], axis=1)
        print(count, key, len(df))
        count+=1
        # generate_wordcloud(monthly_snippets[key])
    df = df.transpose()
    df.sort_index(inplace=True)
    print(df)
    save_file(df, 'dataframe_for_plot.pkl')

def plot_df(df):
    df.plot()
    plt.show()
    return


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')


def stats_tests():
    df = load_file('dataframe_for_plot.pkl')
    df = df.transpose()
    adf_results = []
    # df = df.dropna()
    # df = df.drop([datetime(year=2012,month=2,day=1).date().strftime('%Y-%m-%d %H:%M:%S')], axis=1)
    df.fillna(0, inplace=True)
    # for each row, perform adf test
    # row is a word
    for i in range(0, len(df)):
        data = list(df.iloc[i])
        # smooth data
        data = list(savitzky_golay(np.array(data), 7, 1))
        # add smoothed data
        df.iloc[i] = np.array(data)
        adf_results += [ts.adfuller(data[2:-2])[1]]
    # append results to df
    df['max'] = df.apply(max, axis=1)
    df['adf_results'] = adf_results
    adf_cutoff = sorted(adf_results)[10]
    print(df)
    plot_df(df.loc[(df['adf_results'] < adf_cutoff)].transpose()) # & (df['max'] < 0.0015)].transpose())
    return


analyse_snippets()
stats_tests()

# done


