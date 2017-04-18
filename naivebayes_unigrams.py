# Katherine Kampf
# kkampf
from  __builtin__ import any as b_any
from sets import Set
import sys
import copy
import os
import tweet_process
import operator
import re
import tsv
import glob

# Helper to train classifier
def trainNaiveBayes(training_tweets):

    positive_vocab_size = 0
    negative_vocab_size = 0
    vocab_size = 0
    positive_vocab = dict()
    negative_vocab = dict()
    unique_words = set()
    positive_count = 0
    negative_count = 0

    for tweet in training_tweets:
        tweet_content = tweet[0]
        print positive_count + negative_count
        # calculate counts
        if tweet[1] == "negative":
            negative_count += 1
            for word in tweet_content:
                unique_words.add(word)
                negative_vocab_size += 1
                if word in negative_vocab:
                    negative_vocab[word] += 1
                else:
                    negative_vocab[word] = 1
        else:
            positive_count += 1
            for word in tweet_content:
                unique_words.add(word)
                positive_vocab_size += 1
                if word in positive_vocab:
                    positive_vocab[word] += 1
                else:
                    positive_vocab[word] = 1

    total_tweets = len(training_tweets)
    vocab_size = len(unique_words)
    class_probs = {"positive": float(positive_count)/float(total_tweets), "negative": float(negative_count)/float(total_tweets)}
    return class_probs, negative_vocab, positive_vocab, vocab_size, positive_vocab_size, negative_vocab_size

# Helper to predict positive or negative for a tweet
def testNaiveBayes(test_tweet, negative_vocab, positive_vocab, class_probs, vocab_size,
    positive_vocab_size, negative_vocab_size):

    # calculate probabilities
    negative_prob = class_probs["negative"]
    positive_prob = class_probs["positive"]

    for word in test_tweet:
        # negative probs
        count = 1
        if word in negative_vocab:
            count += negative_vocab[word]
        negative_prob *= float(count)/float(negative_vocab_size + vocab_size)

        # positive probs
        count = 1
        if word in positive_vocab:
            count += positive_vocab[word]
        positive_prob *= float(count)/float(positive_vocab_size + vocab_size)

    if negative_prob > positive_prob:
        return "negative"
    else:
        return "positive"

def contains_positive(tweet_content):
    posmoticons = set([":)", ":-)", ":]", ":-]", ":-3", ":3", ":>", "8)", "8-)", "=-)", ":}", ":-}", "=)", "=]", ":D", ":-D", "xD", "=D", ":/')", ":/'-)"])
    posmojis = set()

    tweet_set = set(tweet_content)
    if posmoticons.intersection(tweet_set):
        print "posmoticon detected"
        return True
    return False

def contains_negative(tweet_content):
    negmojis = set([":(", ":-(", ":c", ":<", ":[", ":-[", ">:[", ">:(", ">:[", ":/'(", ":/'-(", "D:", ":/"])
    tweet_set = set(tweet_content)
    if negmojis.intersection(tweet_set):
        print "negmoji detected"
        return True

    return False

def main():
    # read tweets
    args = list(sys.argv)
    tweet_filename = args[1]
    team_files = glob.glob(args[2] + '/*')

    # append to end of file
    out_file = open('tweet_classifier_unigrams.output', 'w')

    reader = tsv.TsvReader(open(tweet_filename))
    #reader = open(tweet_filename, 'r')

    training_tweets = []
    test_tweets =[]
    count = 0
    for line in reader:
        #line = line.split('    ')
        tweet_class = line[1]
        tweet_string = line[0]
        tweet_content = tweet_process.tweet_process(tweet_string)
        tweet = (tweet_content, tweet_class)
        count += 1
        print count
        training_tweets.append(tweet)

    # train classifier
    class_probs, negative_vocab, positive_vocab, vocab_size, positive_vocab_size, negative_vocab_size \
            = trainNaiveBayes(training_tweets)

    scores = {}

    for f in team_files:
        # get team name from filename
        team = f[4:-10] + '\t'  # <-- the next hot emoticon??? 6roundbreaking

        test = tsv.TsvReader(open(f))
        class_count = {'positive': 0, 'negative': 0}
        total_test = 0
        for tweet in test:
            tweet_content = tweet_process.tweet_process(tweet)
            # run classifier
            class_result = testNaiveBayes(tweet_content, negative_vocab, positive_vocab,
                    class_probs, vocab_size, positive_vocab_size, negative_vocab_size)

            # check for emoticons
            if contains_positive(tweet_content):
                class_result = "positive"
            if contains_negative(tweet_content):
                class_result = "negative"

            class_count[class_result] += 1
            total_test += 1

        pos_percentage = '{0:.2f}% positive'.format(100*(float(class_count['positive']) / float(total_test)))
        neg_percentage = '{0:.2f}% negative'.format(100*(float(class_count['negative']) / float(total_test)))
        scores[team] = {'positive': pos_percentage, 'negative': neg_percentage}

    # out_file.write('Team\n----')
    for team in scores:
        out_file.write(team + pos_percentage + " and " + neg_percentage + '\n\n')

if __name__ == "__main__":
    main()
