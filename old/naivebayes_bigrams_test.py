from pandas import DataFrame
import glob
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from  __builtin__ import any as b_any
from sets import Set
import sys
import copy
import os
#import tweet_process
import operator
import re
import tsv

POSITIVE = 1
NEGATIVE = 0

def build_data_frame(tweet_filename):
    data_frame = DataFrame({'text': [], 'class': []})
    reader = tsv.TsvReader(open(tweet_filename))
    #input_tweet = open(tweet_filename, 'r')
    count = 0
    for line in reader:
	if count % 100000 == 0:
		print count
        tweet_class1 = line[1]
        tweet_string = line[0]
        #tweet_content = tweet_process.tweet_process(tweet_string)
        #tweet_string = " ".join(tweet_content)
        if tweet_class1 == "positive":
            tweet_class = POSITIVE
        if tweet_class1 == "negative":
            tweet_class = NEGATIVE
        data_frame = data_frame.append(DataFrame({'text': [tweet_string], 'class': [tweet_class]}, index=[count]))
        count += 1
    print "done with file processing"
    return data_frame

def main():
    args = list(sys.argv)
    tweet_filename = args[1]
    out_file = open('tweet_classifier.output','w')

    data = DataFrame({'text': [], 'class': []})
    data = data.append(build_data_frame(tweet_filename))
    data = data.reindex(numpy.random.permutation(data.index))
    print "about to do vectorization"
    count_vectorizer = CountVectorizer(ngram_range=(1, 2))
    #count_vectorizer = CountVectorizer()
    counts = count_vectorizer.fit_transform(numpy.asarray(data['text']))
    classifier = MultinomialNB()
    targets = numpy.asarray(data['class'])
    classifier.fit(counts, targets)
    correct_count = 0 
    print "begin classifying"
    test = tsv.TsvReader(open("all_tweets.txt"))
    total_test = 0
    print "bring classifying"
    examples = list()
    for tweet in test:
        tweet_class = tweet[1]
        tweet_string = tweet[0]
        examples.append(tweet_string)
        example_count = count_vectorizer.transform(examples)
        class_results = classifier.predict(example_count)
        class_output = class_results[0]

        # check for accuracy
        if class_output == 1:
            class_result = "positive"
        if class_output == 0:
            class_result = "negative"
        if tweet_class == class_result:
            correct_count += 1
        
        # check for emoticons
        #if contains_positive(tweet_content):
         #   class_result = "positive"
        #if contains_negative(tweet_content):
         #   class_result = "negative"

        # output to file
        #tweet_content = ' '.join(tweet_content)
        out_file.write(tweet_string + " " + class_result + "\n")
        total_test += 1
        examples.pop()

    print correct_count
    print float(correct_count)/float(total_test)

if __name__  == "__main__":
    main()
