import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import json
import time
NFL_TEAMS = ['240734425',  '8824902',  '36375662',  '180503626',  '17076218',  '31126587',  '25084916',  '19853312',  '35865630',  '25545388',  '44666348',  '47964412',  '389038362',  '23642374',  '24109979',  '43403778',  '31504542',  '36155311',  '16347506',  '56443153',  '19426729',  '24179879',  '40358743',  '22146282',  '16332223',  '18734310',  '33583496',  '713143',  '19383279',  '180884045',  '18336787',  '59471027']
'''
access_token = '847977446540533760-7gd4Ojh3Bj9jiELdjoSvw5Nwh9eixS5'
access_token_secret = 'MQ2vOeV2nL6nAJQsKZgCCuQ7pIyCLzMskIKiwbxf1OdR1'
consumer_key = 'soOMSDHcXvi0dEo6ZXZ3DXEUF'
consumer_secret = 'fGJi2zmWx3LCGQHot99Lj7gWPIxqZVY7RY4OxAIX7esIdsoNNy'
'''


class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		
		access_token = '192420553-TmYN5DIzbmifWi7n9SwRlf63f7oC1kriZYbHuaNj'
		access_token_secret = 'yQhylhd4gCKyLT8tc8LTFbXN6bspDKui1Z1S6YInNo0hs'
		consumer_key = 'KyIBorRHHah3H17NN4G1c0ktz'
		consumer_secret = '9YP8eS46zChlMm2jAyUEZzWigHr9GHssDySBg0HDAlgVc09Zm5'
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key='Dh4kxOtgNgiDCx54EAUV3HsQ9'
		consumer_secret='D1BT4k5k63aNcN2llizJfTVo0dFLNo8x6DNcMBEfZQqY7iEhDR'
		access_token='286507548-C8UhCxN7IQnTe9k1DKUHNpnDCHLKrIWIox6PIbvo'
		access_token_secret='PgrTVjLDEDcERCAJiyhfChWucabRxGOqbfOfWBVYk883g'

		access_token = '847977446540533760-7gd4Ojh3Bj9jiELdjoSvw5Nwh9eixS5'
		access_token_secret = 'MQ2vOeV2nL6nAJQsKZgCCuQ7pIyCLzMskIKiwbxf1OdR1'
		consumer_key = 'soOMSDHcXvi0dEo6ZXZ3DXEUF'
		consumer_secret = 'fGJi2zmWx3LCGQHot99Lj7gWPIxqZVY7RY4OxAIX7esIdsoNNy'
		'''
 
		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
		except:
			print("Error: Authentication Failed")

	def is_fan(self,username, team):
		count = 0
		followsTeam = False
		#tweepy.Cursor(self.api.followers_ids, screen_name=username).items():
		#self.api.get_user(username).friends():
		print ("HEREERERE")
		users = []
		for i, page in enumerate(tweepy.Cursor(self.api.friends_ids, id=self.api.get_user(username).id, count=200).pages()):
			for userid in page:
				user = self.api.get_user(userid)
				#print user.screen_name, user.id
				if user.screen_name.lower() == team:
					print username, " follows ", team
					followsTeam = True
				if str(user.id) in NFL_TEAMS and user.screen_name.lower() != team:
					print username, " follows ", user.screen_name, " so is not a fan of ", team
					return False
			time.sleep(.5)

		print "DONE WITH ", username, " followers"
		if followsTeam:
			print username, " is a fan! of ", team 
		else:
			print username, " hates the NFL but tweeted anyways ", team
		return followsTeam

 
	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])\
									|(\w+:\/\/\S+)", " ", tweet).split())
 
	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'
 
	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []
 
		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = query, count = count)
 
			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}
				user = tweet.user.screen_name
				if self.is_fan(user,query[1:]):
					# saving text of tweet
					parsed_tweet['text'] = tweet.text
					# saving sentiment of tweet
					parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
					# appending parsed tweet to tweets list
					if tweet.retweet_count > 0:
						# if tweet has retweets, ensure that it is appended only once
						if parsed_tweet not in tweets:
							tweets.append(parsed_tweet)
					else:
						tweets.append(parsed_tweet)
				print "tweet checked"

 
			# return parsed tweets
			return tweets
 
		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))
 
def main():
	# creating object of TwitterClient Class
	api = TwitterClient()
	
	NFL_HANDLES = []

	
	NFL_HANDLES.append('@giants')
	NFL_HANDLES.append('@dallascowboys')
	NFL_HANDLES.append('@redskins')
	NFL_HANDLES.append('@eagles')

	NFL_HANDLES.append('@nyjets')
	NFL_HANDLES.append('@patriots')
	NFL_HANDLES.append('@buffalobills')
	NFL_HANDLES.append('@miamidolphins')

	NFL_HANDLES.append('@packers')
	NFL_HANDLES.append('@vikings')
	NFL_HANDLES.append('@lions')
	NFL_HANDLES.append('@chicagobears')

	NFL_HANDLES.append('@azcardinals')
	NFL_HANDLES.append('@seahawks')
	NFL_HANDLES.append('@ramsnfl')
	NFL_HANDLES.append('@49ers')

	NFL_HANDLES.append('@saints')
	NFL_HANDLES.append('@tbbuccaneers')
	NFL_HANDLES.append('@atlantafalcons')
	NFL_HANDLES.append('@panthers')

	NFL_HANDLES.append('@steelers')
	NFL_HANDLES.append('@bengals')
	NFL_HANDLES.append('@browns')
	NFL_HANDLES.append('@ravens')

	NFL_HANDLES.append('@raiders')
	NFL_HANDLES.append('@broncos')
	NFL_HANDLES.append('@chiefs')
	NFL_HANDLES.append('@chargers')

	NFL_HANDLES.append('@titans')
	NFL_HANDLES.append('@colts')
	NFL_HANDLES.append('@houstontexans')
	NFL_HANDLES.append('@jaguars')
	
	#for team in NFL_TEAMS:
	#    print api2.get_user(team).screen_name,
	for handle in NFL_HANDLES:
		print handle
		# calling function to get tweets
		tweets = api.get_tweets(query = handle, count = 200)
		#print tweets[0]
		#quit()
		# picking positive tweets from tweets
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
		# percentage of positive tweets
		print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
		# picking negative tweets from tweets
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
		# percentage of negative tweets
		print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
		# percentage of neutral tweets
		print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
	 
		# printing first 5 positive tweets
		print("\n\nPositive tweets:")
		for tweet in ptweets[:10]:
			print(tweet['text'])
	 
		# printing first 5 negative tweets
		print("\n\nNegative tweets:")
		for tweet in ntweets[:10]:
			print(tweet['text'])
 
if __name__ == "__main__":
	# calling main function
	main()





