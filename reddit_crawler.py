"""
    Script to scrape reddit for thread titles.
    Data is pickled.
"""


# need to get comment info as the initial post date might not
# reflect how long the discussion continued


import praw

from util import *
from credentials import *

import math
from datetime import datetime

# can we use the number of comments / upvotes as a measure of impact ??

class RedditCrawler():

    def __init__(self, subreddits, dates):
        # initialise basic props
        self.subreddits = subreddits
        self.dates = dates

    def authenticate(self, client_id, secret):
        """
        Authenticates with Reddit and prepares for data extraction.
        Args:
            client_id:
            secret:

        Returns:

        """
        self.reddit = praw.Reddit(user_agent='Submission extraction',
                                  client_id=client_id,
                                  client_secret=secret)
        return

    def get_comments(self, output='reddit_docs.pkl'):
        """
        For the defined subreddits and dates, downloads
        all top-level comments and saves to specified file.
        Args:
            output: filename str

        Returns:

        """
        if not self.subreddits:
            print("Must set subreddits first")
            return
        self.output = output
        for subreddit in self.subreddits:
            submissions = []
            for submission in self.reddit.subreddit(subreddit).submissions(start=year_to_epoch(self.dates[0]),
                                                              end=year_to_epoch(self.dates[1])
                                                              ):
                # process submission
                submissions += [(submission.id, submission.created, submission.title, submission.num_comments,
                         submission.ups, submission.downs)]
                try:
                    submissions += get_all_comments(submission)
                except:
                    print("comments error")
                print("Current date: ", datetime.fromtimestamp(submission.created).strftime('%Y %m %d'))
            # dump completed output to pickle file
            save_file(submissions, output)
            print(subreddit+" complete.")
        # send final output to user
        print("All subreddits completed.")
        return

    def get_submissions(self, output='reddit_docs.pkl'):
        """
        For the defined subreddits and dates, downloads
        all submissions and saves to specified file.
        Args:
            output: filename str

        Returns:

        """
        self.output = output
        if not self.subreddits:
            print("Must set subreddits first")
            return
        for subreddit in self.subreddits:
            submissions = []
            for submission in self.reddit.subreddit(subreddit).submissions(start=year_to_epoch(self.dates[0]),
                                                              end=year_to_epoch(self.dates[1])
                                                              ):
                # process submission
                submissions += [(submission.id, submission.created, submission.title, submission.num_comments,
                         submission.ups, submission.downs)]
                print("Current date: ", datetime.fromtimestamp(submission.created).strftime('%Y %m %d'))
            # dump completed output to pickle file
            save_file(submissions, output)
            print(subreddit+" complete.")
        # send final output to user
        print("All subreddits completed.")
        return

    def prepare_snippets(self, file_name=self.output, output='reddit_for_analysis.pkl'):
        """
        Converts reddit docs to Snippet form for
        processing in main script.
        Args:
            file_name: str
            output: str

        Returns:

        """
        submissions = load_file(file_name)
        snippets = [(s[1], s[2], round(math.log(s[3]+1))+1) for s in submissions]
        save_file(snippets, output)
        print("Final file saved to ", output)
        return

    def year_to_epoch(self, year):
        return datetime.strptime(year, '%Y').timestamp()

    def get_all_comments(self, submission, limit=0):
        """
        Return all comments for a submission.
        Args:
            submission: instance of reddit submission
            limit: int max number of requests to use

        Returns: list of reddit docs

        """
        if not isinstance(submission, praw.models.Submission):
            print("Must provide submission instance")
            raise TypeError
        submission.comments.replace_more(limit=limit)
        comments = []
        for comment in submission.comments.list():
            comments += [(comment.id, comment.created, comment.body, None, comment.ups, comment.downs)]
        return comments


reddit_crawler = RedditCrawler(['education'], ['2015', '2016'])

reddit_crawler.authenticate(reddit_client_id, reddit_secret)

reddit_crawler.get_submissions('test.pkl')


