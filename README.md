WIP
# Trend Predictor
Analyse data for upcoming (long-term) trends in a particular industry.

The current build figures out what people have been talking about online and then tries to see if anything is growing in popularity/usage - this is a 'trend'. 

This model is not suitable for monitoring short term trends such as most popular products in beauty. It is particularly designed to monito long term trends that last for at least one year. Example trends for the education industry include: classroom tablets, coding courses, split-gender schooling.

## Structure
The overall structure of the model is:
1. Extract online discussions / commentary on the industry via keyword monitoring and save these as json files with added information (e.g. who posted, date posted, importance/weight), e.g.
  - Reddit: submissions and comments
  - Twitter: tweets
  - forums: posts
  - Instagram: posts
 
2. Process data to create a standard format across different platforms, the "Snippet". Processes include:
  - clean (remove links, tags)
  - filter out irrelevant discussions
  - find points of speech and identify important parts of sentence
  - lemmatize / stem
  - remove stop words (industry specific)

3. Generate a multi-platform time-series for each term in the data set:
  - divide Snippets into monthly buckets
  - combine Snippets into one doc for processing
  - calculate frequency distributions with weightings
  - combine monthly data to form time series
  - normalise each term with total terms per monh (remove effects of growing discussion size, want to capture which % of discussion is devoted to topic)

4. Detect Increases:
  - apply a smoothing filter (The time series is smoothed with a linear Savitzky Golay filter to remove any minor fluctuations. The filter is a convolutional filter which performs sucessive linear least-squares fit on adjacent points. For this problem, we use a seven month window and a second order polynomial to account for typical monthly variations that occur in what we expect to be exponential growth (on the scale of years))
  - check for increasing non-stationarity (Next an Augmented Dickey Fuller test is applied to check for stationarity (whether or not the process has any underlying trend in time). This test basically checks if a previous data point can affect the next data point; in the case of stationarity a high point is likely to be followed by a low point in order to move back towards the trending mean, on the otherhand, in athe case of a non-stationary process the probability of a point being low or high will not depend on the previous point.)

5. Perform sanity check:
  - plot each term
  - check other data sources
  - look at high-weighted Snippets

## Data Sources

Data comes from:
- twitter (via tweepy)
- reddit (via PRAW)
- google trends (via pytrends) - what are people searching for?
- white papers - what are scholars discussing?
- forums (scraped)
- instagram - popular pictures
- google adwords - what do advertisers think?

### Reddit Crawler
The Reddit crawler accesses Reddit through the PRAW library. The crawler takes subreddit names and dates and crawls the subreddit between those dates, extracting all the submissions and top-level comments. The crawler extracts the date, title/comment along with the upvotes/downvotes and number of comments. The crawler then converts the data into the Snippet structure (date, text, weight) used by the trend-predictor.

Running with subreddit 'education' for 2012-2016 results in 20 thousand submissions with 100 thousand snippets and over 6 million words.


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
- Influencer locator: create a module that will hunt influencers.
- Noun Phrases: textblob can search for noun phrases within sentences which would better identify the higher level concepts but this runs very slowly on a local PC - is there another solution to incorporate higher level meanings? Nounphrases are good because they reduce the dimensionality of our data, leading to faster training.
- wordnets.synsets: Use synonyms to further reduce dimensionality of corpus.
- predefined term calculator: e.g. topia.termextract can find the best terms in a sentence based on frequency, possible more efficient than own.
- country specific: could be very important to filter out discussions from certain countries, e.g. developing very different to developed for education.
- Stationarity: ADF doesn't seem to be a good indicator of a trend, what else could be used?
- Thought leader identifier: Listening to the masses gives us a large selection of data but it also introduces a lot of noise. It would be better to define a thought leader and weight their conversations accordingly. Leaders can be identified by number of relevant posts (using hashtags / keywords), number of followers, number of times they're mentioned in other posts. This can then be recursively grown by finding the people they are most linked to.
- Weights: certain comments / sources should have a higher weight than others.
- Short-term trend predictor: this may have more realisable applications, e.g. becoming a trend-setter. Genral idea: calculate different features for each term and train classifier on past trends to see if certain features are good indicators of lift-off. Previous trends can be seen as a peak. We want to discover factors that lead to that, before the peak. Word popularity is just one factor. Number of influencers discussion, conference papers. For each term, define period where it was trending / not trending, this provides labeled dataset for training (0 never trend, 1 became trend and then data is previous 6 months), and, the number of current trends may be an indicator of the likelihood of success of a term, more likely on the tail end.
- Snippet example extractor: for the terms which were found to be trends, look at the high-weighted Snippets where it was used - does it make sense?
