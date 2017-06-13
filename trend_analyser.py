from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

import statsmodels.tsa.stattools as ts

import pandas as pd

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
    return "".join([(s[1]+' ')*int(s[2]) for s in snippets])


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
    cached_stop_words = set(stopwords.words("english"))
    cached_stop_words.update(['education','&','-','--','2012','8','america','american'])
    doc = ' '.join([word for word in doc.split() if word.lower() not in cached_stop_words])
    return doc


def create_counts(doc):
    """
    Create a frequency distribution from a doc.

    Args:
        doc: string

    Returns: dict containing counts of top 100 terms

    """
    freqs = Counter(doc.lower().split()).most_common(100)
    # normalise
    for i in range(0, len(freqs)):
        freqs[i] = (freqs[i][0], freqs[i][1] / len(doc.split()))
    return freqs


def analyse_tweets():
    snippets = load_file('reddit_for_analysis.pkl')
    # divide monthly
    monthly_snippets = divide_monthly(snippets)
    df = pd.DataFrame()
    # convert to docs and stem
    for key in monthly_snippets.keys():
        monthly_snippets[key] = stem_doc(remove_stop_words(snippets_to_doc(monthly_snippets[key])))
        counts = create_counts(monthly_snippets[key])
        df_temp = pd.DataFrame([(key, c[0], c[1]) for c in counts])
        df_temp = df_temp.pivot(index=1, columns=0, values=2)
        df = pd.concat([df, df_temp], axis=1)
        print(key, df)
        # generate_wordcloud(monthly_snippets[key])
    df = df.transpose()
    df.sort_index(inplace=True)
    print(df)
    save_file(df, 'dataframe_for_plot.pkl')


def stats_tests():



analyse_tweets()


# done


