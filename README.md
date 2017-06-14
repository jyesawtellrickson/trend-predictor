WIP


Analyse data for upcoming trends in a particular industry.

Data comes from:
- twitter (via tweepy)
- reddit (via PRAW)
- google trends (via pytrends)
- forums (scraped)
- teaching plans

## Education
Start by looking at what adults are speaking about in the industry. Search Twitter for the education hashtag, try to identify thought leaders in the area. Generate a corpus from their tweets and track the most talked about topics by month/year. Perform a similar analysis of the blogs and teaching forums.

Look at sentiment of students talking about school, how has it changed throughout the trends.

For content changes we can analyse teaching plans.


# Crawlers

## Reddit Crawler
The Reddit crawler accesses Reddit through the PRAW library. The crawler takes subreddits names and dates and crawls the subreddit between those dates, extracting all the submissions and top-level comments. The crawler extracts the date, title/comment along with the upvotes/downvotes and number of comments. The crawler then converts the data into the Snippet structure (date, text, weight) used by the trend-predictor.

# Trend Analyser

In order to pick up trends, the trend analyser takes in a large collection of dated documents and analyses these to find terms which are 'trending'. The first step is to clean up the Snippets, this is done by removing stop words (including custom ones for the industry) and links and then stemming the remaining words. Next, counts of each term are generated and the top terms are taken for each month. The monthly counts are then combined to form a time series. 

The time series is smoothed with a linear Savitzky Golay filter (6 month window) to remove any minor fluctuations then an Augmented Dickey Fuller test is applied to check for stationarity. Terms which are shown to be non-stationary are then plotted for further analysis.
