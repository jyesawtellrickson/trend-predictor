from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

from textblob import TextBlob

import statsmodels.tsa.stattools as ts
from scipy.signal import savgol_filter
import numpy as np

import pandas as pd

from nltk.stem.porter import *
import string

from collections import Counter

from datetime import datetime
from dateutil.relativedelta import *

from util import *


class TrendAnalyser:

    def __init__(self):
        self.data = []
        self.sources = []
        self.default_sources = {'reddit': 'reddit_for_analysis.pkl'}
        self.time_series_file = 'time_series.pkl'

    def load_source(self, source, location=None):
        if location:
            self.data += load_file(location)
        else:
            self.data += load_file(self.default_sources[source])
        self.sources += [source]
        return

    @classmethod
    def clean_data(cls, data):
        """
        Take in data as snippets and return list of noun phrases
        Args:
            data:

        Returns:

        """
        return cls.get_noun_phrases(cls.snippets_to_doc(data))

    def create_time_series(self):
        # collect data
        snippets = self.data
        # divide monthly
        monthly_snippets = self.divide_monthly(snippets)
        df = pd.DataFrame()
        count = 0
        # convert to docs and stem
        print("Generating time series")
        for key in monthly_snippets.keys():
            # monthly_snippets[key] = stem_doc(remove_stop_words(snippets_to_doc(monthly_snippets[key])))
            # counts = create_counts(monthly_snippets[key])
            monthly_snippets[key] = self.clean_data(monthly_snippets[key])
            counts = self.counts_from_list(monthly_snippets[key])
            df_temp = pd.DataFrame.from_dict(counts, orient='index')
            df_temp.columns = [key]
            df = pd.concat([df, df_temp], axis=1)
            # print(count, key, len(df))
            count += 1
        df = df.transpose()
        df.sort_index(inplace=True)
        save_file(df, self.time_series_file)
        print('Time series successfully created')
        return


    @staticmethod
    def plot_time_series(df):
        """
        Create a line plot of the time series DataFrame
        Args:
            df (DataFrame):
        """
        # Remove excess data
        df = df[:-4]
        # Normalise
        max_val = max(df.apply(np.max))
        df = df.apply(lambda x:  x/max_val)
        time_series_plot = df.plot(kind='line',
                                   figsize=(20, 15),
                                   fontsize=15)
        plt.xlabel('Month', fontsize=20)
        plt.ylabel('Popularity', fontsize=20)
        plt.title('Historical Word Popularity', fontsize=25)
        plt.show()
        return

    @staticmethod
    def plot_df(df):
        """
        Create a line plot of the DataFrame
        Args:
            df (DataFrame):
        """
        df.plot()
        plt.show()
        return

    def stats_tests(self):
        df = load_file(self.time_series_file)
        df = df.transpose()
        adf_results = []
        up = []
        maxim = []
        average = []
        # df = df.dropna()
        # df = df.drop([datetime(year=2012,month=2,day=1).date().strftime('%Y-%m-%d %H:%M:%S')], axis=1)
        df.fillna(0, inplace=True)
        # for each row, perform adf test
        # row is a word
        print("Running statistics tests")
        for i in range(0, len(df)):
            if i % 20 == 0:
                print("  {:.1%} complete".format(i/len(df)))
            data = list(df.iloc[i])
            # smooth data
            data = list(savgol_filter(np.array(data), 7, 2))
            # add smoothed data
            df.iloc[i] = np.array(data)
            data = data[2:-2]
            adf_results += [ts.adfuller(data)[1]]
            up += [(sum(data) - 2 * sum(data[0:int(len(data)/2)]))/sum(data)]
            maxim += [max(data)]
            average += [sum(data)/len(data)]
        # append results to df
        df['up'] = up
        df['average'] = average
        df['max'] = maxim  # df.apply(max, axis=1)
        df['adf_results'] = adf_results
        adf_cutoff = sorted(adf_results)[20]
        print("Statistics tests complete")
        self.plot_time_series(df.loc[(df['up'] > 0.1) & (df['average'] > 0.001)].transpose())  # & (df['max'] < 0.0015)].transpose())
        # self.plot_time_series(df.loc[(df['up'] > 0) & (df['average'] > 0.001)plot_df & (df['adf_results'] < 0.1)].transpose())  # & (df['max'] < 0.0015)].transpose())
        return

    # Data clean-up
    @classmethod
    def get_noun_phrases(cls, doc):
        print(len(doc))
        doc = doc[:min(1000000, len(doc))]
        doc = cls.remove_punctuation(doc)
        blob = TextBlob(doc)
        ans = [b[0] for b in blob.tags if b[1].find('NN') >= 0]
        # ans2 = blob.noun_phrases
        return ans

    @staticmethod
    def remove_punctuation(doc):
        return doc.translate(str.maketrans({key: None for key in string.punctuation}))

    @classmethod
    def stem_doc(cls, doc):
        """
        Takes a doc and applies stemming to words.
        Args:
            doc: string

        Returns: stemmed doc string

        """
        stemmer = PorterStemmer()
        doc = cls.remove_punctuation(doc)
        words = [stemmer.stem(word) for word in doc.split()]
        return ' '.join(words)

    @staticmethod
    def remove_stop_words(doc):
        """
        Remove stopwords from a doc
        Args:
            doc: string

        Returns: string

        """
        cached_stop_words = set(stopwords.words("english"))
        cached_stop_words.update(['education', 'america', 'american', 'always',
                                  'back', "didn't", 'end', 'even', 'get', 'job', 'need', 'them', 'there',
                                  'that', "can't", 'day', "didn't", "don't", 'get', 'give', "i've", 'me',
                                  'sure', 'that', 'two'])
        doc = ' '.join([word for word in doc.split() if word.lower() not in cached_stop_words])
        return doc

    # Plotting
    @staticmethod
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

    # Helper
    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def create_counts(doc, count=200):
        """
        Create a frequency distribution from a doc.

        Args:
            doc: string
            count: int number of terms to return

        Returns: dict containing counts of terms

        """
        # limit size of doc or else it breaks on MemoryError
        try:
            doc = doc.lower().split()
        except MemoryError:
            doc = doc[0:7000000]
            doc = doc.lower().split()
        freqs = dict(Counter(doc).most_common(count))
        # normalise
        for word in freqs.keys():
            freqs[word] /= len(doc)
        return freqs

    @staticmethod
    def counts_from_list(doc, count=200):
        """
        Takes a doc and returns the counts of
        the most occuring words.
        Args:
            doc (string):
            count (int): the number of terms to return

        Returns: dict of counts

        """
        freqs = dict(Counter(doc).most_common(count))
        for word in freqs.keys():
            freqs[word] /= len(doc)
        return freqs
