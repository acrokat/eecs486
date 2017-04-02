import sys

def read_tweets(filename):
    f = open(filename, 'r')
    annotated_tweets = []
    for line in f.readlines():
        annotated_tweets.append((line.split('    ')[0].strip(), line.split('    ')[1].strip()))

    for t in annotated_tweets:
        print t[0], '  ', t[1]

if __name__ == '__main__':
    filename = sys.argv[1]
    read_tweets(filename)
