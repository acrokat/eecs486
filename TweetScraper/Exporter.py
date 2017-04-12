# -*- coding: utf-8 -*-

import sys,getopt,got,datetime,codecs

def main(argv, fileName):
	
	

	if len(argv) == 0:
		print 'You must pass some parameters. Use \"-h\" to help.'
		return
		
	if len(argv) == 1 and argv[0] == '-h':
		print """\nTo use this jar, you can pass the folowing attributes:
    username: Username of a specific twitter account (without @)
       since: The lower bound date (yyyy-mm-aa)
       until: The upper bound date (yyyy-mm-aa)
 querysearch: A query text to be matched
   maxtweets: The maximum number of tweets to retrieve

 \nExamples:
 # Example 1 - Get tweets by username [barackobama]
 python Exporter.py --username "barackobama" --maxtweets 1\n

 # Example 2 - Get tweets by query search [europe refugees]
 python Exporter.py --querysearch "europe refugees" --maxtweets 1\n

 # Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']
 python Exporter.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1\n
 
 # Example 4 - Get the last 10 top tweets by username
 python Exporter.py --username "barackobama" --maxtweets 10 --toptweets\n"""
		return
 
	try:
		opts, args = getopt.getopt(argv, "", ("username=", "since=", "until=", "querysearch=", "toptweets", "maxtweets="))
		
		tweetCriteria = got.manager.TweetCriteria()
		
		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg
				
			elif opt == '--since':
				tweetCriteria.since = arg
				
			elif opt == '--until':
				tweetCriteria.until = arg
				
			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg
				
			elif opt == '--toptweets':
				tweetCriteria.topTweets = True
				
			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
				
		
		outputFile = codecs.open(fileName, "w+", "utf-8")
		
		#outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink')
		
		print 'Searching...\n'
		
		def receiveBuffer(tweets):
			for t in tweets:
				#outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink)))
				outputFile.write('%s\n'%t.text)
			outputFile.flush();
			print 'More %d saved on file...\n' % len(tweets)
		
		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		
	except arg:
		print 'Arguments parser error, try -h' + arg
	finally:
		outputFile.close()
		print 'Done. Output file generated.', fileName

if __name__ == '__main__':
	NFL_HANDLES = []
	'''
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
	'''
	NFL_HANDLES.append('@jaguars')
	NFL_HANDLES.append('@houstontexans')
	NFL_HANDLES.append('@houstontexans')
	ins = sys.argv
	for handle in NFL_HANDLES:
		
		ins[2] = handle
		fileName = str(handle[1:])+"Tweets.txt"
		main(ins[1:],fileName)
		#quit()





