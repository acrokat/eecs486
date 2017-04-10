# Katherine Kampf
# kkampf

import sys
import copy
import os
import tweet_process
import operator
import re
import tsv

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

def main():
    # read tweets
    args = list(sys.argv)
    tweet_filename = args[1]
    
    out_file = open('tweet_classifier.output','w')

    # parse tweets using first 3/4 for training and 1/4 for test
    NUM = 1220
    count = 0
    reader = tsv.TsvReader(open(tweet_filename))
    training_tweets = []
    test_tweets =[]
    for line in reader:
        tweet_class = line[1]
        tweet_string = line[0]
        tweet_tokens = tweet_string.split()
        tweet_content = tweet_process.tweet_process(tweet_tokens)
        tweet = (tweet_content, tweet_class)

        if count < NUM:
            training_tweets.append(tweet)
        else:
            test_tweets.append(tweet)
        count += 1
    
    # train classifier
    class_probs, negative_vocab, positive_vocab, vocab_size, positive_vocab_size, negative_vocab_size \
            = trainNaiveBayes(training_tweets)

    correct_count = 0
    for tweet in test_tweets:
        tweet_tokens = tweet[0]

        # run classifier
        class_result = testNaiveBayes(tweet_content, negative_vocab, positive_vocab, 
                class_probs, vocab_size, positive_vocab_size, negative_vocab_size)

        # check for accuracy
        if tweet[1] == class_result:
            correct_count += 1

        # output to file
        tweet_content = ' '.join(tweet_tokens)
        out_file.write(tweet_content + " " + class_result + "\n")

    print float(correct_count)/float(len(test_tweets))

if __name__  == "__main__":
    main()

