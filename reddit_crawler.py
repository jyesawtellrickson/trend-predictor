"""
    Script to scrape reddit for thread titles.
    Data is pickled in a pandas dataframe as well as
    being saved as a csv.
"""

import bs4
import requests
import pandas as pd
import pickle as pkl

# can we use the number of comments / upvotes as a measure of impact ??

# define subreddits to scrape
subreddits = ['teaching', 'education']
posts = []
# process each country seperately
for subreddit in subreddits:
    # define base website address and search address
    base = 'https://www.reddit.com/r/' + subreddit
    # iterate through pages, using count and after to get right page
    search = True
    params = {'count': 0, 'after': ''}
    while search == True:
        print("Processing Page: {0}".format(params['count']/25))
        page = requests.get(base, params)
        # convert to soup
        homeSoup = bs4.BeautifulSoup(page.text)
        # get card elements
        elems = homeSoup.find_all('div', attrs={"class": 'thing'})
        # iterate through elements
        for elem in enumerate(elems):
            # get title, date
            posts += [elem]
    # dump completed output to caterers pickle file
    pkl.dump(posts, open("reddit_posts.pkl", "wb"))
    print(subreddit+" complete.")
# send final output to user
print("All subreddits completed.")