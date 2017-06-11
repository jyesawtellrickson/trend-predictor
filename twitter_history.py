from twitter import *

token = "899746063-eTIFXfPAhbZiwIzJDDpFVdwP54IE2m2KDPsF2NMf"
token_secret = "vyp0wZY8H2uccAFE1I8dx6OuFAMAZCPPPuuY4A1mAt1bt"
consumer_key = "aTBKDuDix3ILWXdCSMC2rwoUV"
consumer_secret = "wBdoCAXY7lkL0QDBy5IsE6zbDk9BowJksMIKwafKn0JvWvkh4B"

t = Twitter(
    auth=OAuth(token, token_secret, consumer_key, consumer_secret))

# Get your "home" timeline
#timeline = t.statuses.home_timeline(count=5)

# get all tweets with hashtag education
education = t.search.tweets(q="#education since:2017-01-01", length=200)


print(education)

thefile = open('output.txt', 'w')

thefile.write(education)

thefile.close()




#######

from pytrends import *

pytrends = TrendReq(google_username, google_password, hl='en-US', tz=360, custom_useragent=None)
pytrends = build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
pytrends.interest_over_time()
pytrends.related_queries()


