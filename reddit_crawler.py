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
            # get tag as string
            name = elem.a.getText()
            tag = str(elem.p)[3:-4]
            temp = str(elem.a).find(">")
            link = str(elem.a)[9:temp-1]
            caterers.loc[start_p+j] = [name, tag, base+link]
    # dump completed output to caterers pickle file
    pkl.dump(caterers, open("caterers_"+country+".p", "wb"))
    # also send to csv
    caterers.to_csv("caterers_"+country+".csv", encoding='utf-8')
    print(country+" complete.")
# send final output to user
print("All countries completed.")