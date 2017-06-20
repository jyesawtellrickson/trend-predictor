WIP
# Trend Predictor
Analyse data for upcoming trends in a particular industry.

Data comes from:
- twitter (via tweepy)
- reddit (via PRAW)
- google trends (via pytrends)
- forums (scraped)

The current build figures out what people have been talking about online and then tries to see if anything is growing in popularity/usage - this is a 'trend'.

## Crawlers

### Reddit Crawler
The Reddit crawler accesses Reddit through the PRAW library. The crawler takes subreddit names and dates and crawls the subreddit between those dates, extracting all the submissions and top-level comments. The crawler extracts the date, title/comment along with the upvotes/downvotes and number of comments. The crawler then converts the data into the Snippet structure (date, text, weight) used by the trend-predictor.

Running with subreddit 'education' for 2012-2016 results in 20 thousand submissions with 100 thousand snippets and over 6 million words.

## Trend Analyser

In order to pick up trends, the trend analyser takes in a large collection of dated documents and analyses these to find terms which are 'trending'. The first step is to clean up the Snippets, this is done by removing stop words (including custom ones for the industry) and links and then stemming the remaining words. Next, counts of each term are generated and the top terms are taken for each month. The monthly counts are then combined to form a time series. 

The time series is smoothed with a linear Savitzky Golay filter to remove any minor fluctuations. The filter is a convolutional filter which performs sucessive linear least-squares fit on adjacent points. For this problem, we use a seven month window and a second order polynomial to account for typical monthly variations that occur in what we expect to be exponential growth (on the scale of years).

Next an Augmented Dickey Fuller test is applied to check for stationarity (whether or not the process has any underlying trend in time). This test basically checks if a previous data point can affect the next data point; in the case of stationarity a high point is likely to be followed by a low point in order to move back towards the trending mean, on the otherhand, in athe case of a non-stationary process the probability of a point being low or high will not depend on the previous point.

If a word can be shown to be non-stationary and increasing then we would expect this to be an upcoming trend. Terms which are shown to be non-stationary are plotted for further analysis.

## Industry

### Education
Start by looking at what adults are speaking about in the industry. Search Twitter for the education hashtag, try to identify thought leaders in the area. Generate a corpus from their tweets and track the most talked about topics by month/year. Perform a similar analysis of the blogs and teaching forums.

Look at sentiment of students talking about school, how has it changed throughout the trends.

For content changes we can analyse teaching plans.

## Countributing
Things I'd like to do:
- Reddit Crawler: retrieve all comments, not just top-level (need to deal with rate limits)
- Feature predictor: We should create features for prominince, popularity etc. for terms on all the different platforms and then this can be used along with values from previous trends which did become popular to try to identify what are the features that lead to tipping point. Could use a search tree (trend/not) or a linear regressor (score indicating trendiness).
- Popular comment generator: train a model to predict the popularity of a comment/post then build one to become popular. This sort of linguistic model won't help predict any trends though.
- Account for seasonal affects
- Twitter Crawler: need to get data only from particular dates and only up to a certain number. Is there a way to get around their API limitations?
- Noun Phrases: textblob can search for noun phrases within sentences which would better identify the higher level concepts but this runs very slowly on a local PC - is there another solution to incorporate higher level meanings?
- Stationarity: ADF doesn't seem to be a good indicator of a trend, what else could be used?
- Thought leader identifier: Listening to the masses gives us a large selection of data but it also introduces a lot of noise. It would be better to define a thought leader and weight their conversations accordingly. Leaders can be identified by number of relevant posts (using hashtags / keywords), number of followers, number of times they're mentioned in other posts. This can then be recursively grown by finding the people they are most linked to.
- Weights: certain comments / sources should have a higher weight than others.
