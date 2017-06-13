"""
    Script to scrape reddit for thread titles.
    Data is pickled.
"""

import praw
from util import *
from credentials import *

import math
from datetime import datetime

# can we use the number of comments / upvotes as a measure of impact ??

def monthly_buckets(timeframes):
    """

    Args:
        timeframes: list of start/end data

    Returns: month buckets

    """
    return

def year_to_epoch(year):
    return datetime.strptime(year, '%Y').timestamp()


# define subreddits to scrape
subreddits = ['teaching', 'education']
posts = []
timeframes = ['2012', '2016']

reddit = praw.Reddit(user_agent='Submission extraction', client_id=reddit_client_id,
                     client_secret=reddit_secret)

# process each country seperately
for subreddit in subreddits:
    submissions = []
    for submission in reddit.subreddit(subreddit).submissions(start=year_to_epoch(timeframes[0]),
                                                              end=year_to_epoch(timeframes[1])
                                                              ):
        # process submission
        submissions += [(submission.id, submission.created, submission.title, submission.num_comments,
                         submission.ups, submission.downs)]
        print(datetime.fromtimestamp(submission.created).strftime('%Y %m %d'))
    # dump completed output to caterers pickle file
    save_file(submissions, 'reddit_2_'+subreddit+'_submissions.pkl')
    print(subreddit+" complete.")
# send final output to user
print("All subreddits completed.")


def prepare_reddit_corpus():
    submissions = load_file('reddit_2_education_submissions.pkl')
    # put in same format as others
    docs = [(s[1], s[2], round(math.log(s[3]+1))+1) for s in submissions]
    save_file(docs, 'reddit_for_analysis.pkl')
    return

