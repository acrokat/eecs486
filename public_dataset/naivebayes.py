# Katherine Kampf
# kkampf

import sys
import copy
import os
from preprocess import *
import operator
import re
import csv

# Helper to train classifier
def trainNaiveBayes(files, training_tweets):

    positive_vocab_size = 0
    negative_vocab_size = 0
    vocab_size = 0
    positive_vocab = dict()
    negative_vocab = dict()
    unique_words = set()
    positive_count = 0
    negative_count = 0

    for tweet in training_tweets:

        # calculate counts
        if tweet[1] == "negative":
            negative_count += 1
            for word in tweet:
                unique_words.add(word)
                negative_vocab_size += 1
                if word in negative_vocab:
                    negative_vocab[word] += 1
                else:
                    negative_vocab[word] = 1
        else:
            positive_count += 1
            for word in new_tokens:
                unique_words.add(word)
                positive_vocab_size += 1
                if word in positive_vocab:
                    positive_vocab[word] += 1
                else:
                    positive_vocab[word] = 1

    total_docs = len(files)
    vocab_size = len(unique_words)
    class_probs = {"positive": float(positive_count)/float(total_docs), "negative": float(negative_count)/float(total_docs)}
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
    count = 0
    with open(tweet_filename,'r') as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            # TODO: preprocess
            tweet_class = line[4]
            # only include psoitive/negative examples
            if tweet_class == "objective":
                break
            tweet_content = line[5]
            tweet = (tweet_content, tweet_class)
            # TODO: replace NUM with how many tweets we want as training
            if count < NUM:
                training_tweets.append(tweet)
            else:
                test_tweets.append(tweet)
            count++
    
    # train classifier
    class_probs, negative_vocab, positive_vocab, vocab_size, positive_vocab_size, negative_vocab_size \
            = trainNaiveBayes(training_files, training_tweets)

    for tweet in test_tweets:

        # run classifier
        class_result = testNaiveBayes(tweet, negative_vocab, positive_vocab, test_tweets, 
                class_probs, vocab_size, positive_vocab_size, negative_vocab_size)

        # check for accuracy
        if tweet[1] == class_result:
            correct_count += 1

        # output to file
        out_file.write(tweet + " " + class_result + "\n")

    print float(correct_count)/float(len(files))

if __name__  == "__main__":
    main()

