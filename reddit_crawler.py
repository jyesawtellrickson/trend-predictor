"""
    Script to scrape reddit for thread titles.
    Data is pickled.
"""
import praw

from util import *

from math import log
from datetime import datetime


class RedditCrawler:

    def __init__(self, subreddits, dates, reddit_file='reddit_file.pkl', snippet_file='reddit_snippet_file.pkl'):
        # initialise basic props
        self.reddit = None
        self.subreddits = subreddits
        self.dates = dates
        self.reddit_file = reddit_file
        self.snippet_file = snippet_file

    def authenticate(self, client_id, secret):
        """
        Authenticates with Reddit and prepares for data extraction.
        Args:
            client_id:
            secret:

        Returns:

        """
        try:
            self.reddit = praw.Reddit(user_agent='Submission extraction',
                                      client_id=client_id,
                                      client_secret=secret)
            print("Client authenticated")
        except:
            print("Client failed to authenticate")
        return

    def get_comments(self):
        """
        For the defined subreddits and dates, downloads
        all top-level comments and saves to pickle file.
        """
        if not self.reddit:
            print("Authenticate first")
            return
        if not self.subreddits:
            print("Must set subreddits first")
            return
        submissions = []
        for subreddit in self.subreddits:
            for submission in self.reddit.subreddit(subreddit).submissions(
                    start=self.year_to_epoch(self.dates[0]),
                    end=self.year_to_epoch(self.dates[1])):
                # process submission
                submissions += [(submission.id, submission.created, submission.title, submission.num_comments,
                                 submission.ups, submission.downs)]
                try:
                    submissions += self.get_all_comments(submission)
                except:
                    print("comments error")
                print("Current date: ", datetime.fromtimestamp(submission.created).strftime('%Y %m %d'))
            print(subreddit+" complete.")
        # dump completed output to pickle file
        save_file(submissions, self.reddit_file)
        # send final output to user
        print("All subreddits completed.")
        return

    def get_submissions(self):
        """
        For the defined subreddits and dates, downloads
        all submissions and saves to pickle file.
        """
        if not self.reddit:
            print("Authenticate first")
            return
        if not self.subreddits:
            print("Must set subreddits first")
            return
        submissions = []
        for subreddit in self.subreddits:
            for submission in self.reddit.subreddit(subreddit).submissions(
                    start=self.year_to_epoch(self.dates[0]),
                    end=self.year_to_epoch(self.dates[1])):
                # process submission
                submissions += [(submission.id, submission.created, submission.title, submission.num_comments,
                                 submission.ups, submission.downs)]
                print("Current date: ", datetime.fromtimestamp(submission.created).strftime('%Y %m %d'))
            print(subreddit+" complete.")
        # dump completed output to pickle file
        save_file(submissions, self.reddit_file)
        # send final output to user
        print("All subreddits completed.")
        return

    def prepare_snippets(self):
        """
        Converts reddit docs to Snippet form for
        processing in main script. File saved to pickle.
        """
        submissions = load_file(self.reddit_file)
        snippets = [(s[1], s[2], round(log(s[3]+1))+1) for s in submissions]
        save_file(snippets, self.snippet_file)
        print("Final file saved to ", self.snippet_file)
        return

    @staticmethod
    def year_to_epoch(year):
        return datetime.strptime(year, '%Y').timestamp()

    @staticmethod
    def get_all_comments(submission, limit=0):
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



