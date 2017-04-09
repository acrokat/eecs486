# returns dictionary {tweet: class}
# uncomment 'annotated_tweets' comments and return annotated_tweets
# for a list of tuples (tweet, class) instead
def read_tweets(filename):
    f = open(filename, 'r')
    #annotated_tweets = []
    tweets = {}
    for line in f.readlines():
        split_line = line.split('    ')
        #annotated_tweets.append((split_line[0].strip(), split_line[1].strip()))
        tweets[split_line[0].strip()] = split_line[1].strip()
        #annotated_tweets.append(tweet)

    return tweets
    #annotated_tweets
if __name__ == '__main__':
    filename = sys.argv[1]
    tweet_tuples = read_tweets(filename)
