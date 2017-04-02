import json
from time import sleep

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '847977446540533760-7gd4Ojh3Bj9jiELdjoSvw5Nwh9eixS5'
ACCESS_SECRET = 'MQ2vOeV2nL6nAJQsKZgCCuQ7pIyCLzMskIKiwbxf1OdR1'
CONSUMER_KEY = 'soOMSDHcXvi0dEo6ZXZ3DXEUF'
CONSUMER_SECRET = 'fGJi2zmWx3LCGQHot99Lj7gWPIxqZVY7RY4OxAIX7esIdsoNNy'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twitter(auth=oauth, retry=True)

f = open('nfc_east.txt', 'w')
tweet_set = set()
teams = ['@dallascowboys', '@Giants', '@Redskins', '@Eagles']

while len(tweet_set) < 150:
    for team in teams:
        tweets = twitter.search.tweets(q=team, lang='en')
        statuses = tweets['statuses']

        for status in statuses:
            if 'RT' not in status['text']:
                encoded_tweet = status['text'].replace('\n', ' ').encode('utf-8')
                if encoded_tweet in tweet_set:
                    sleep(5)
                else:
                    tweet_set.add(encoded_tweet)
                    print encoded_tweet

for tweet in tweet_set:
        print>>f, tweet
