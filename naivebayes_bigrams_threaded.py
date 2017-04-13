from pandas import DataFrame
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from  __builtin__ import any as b_any
from sets import Set
import sys
import copy
import os
import tweet_process
import operator
import re
import tsv
from multiprocessing import Process, Queue
import glob
import threading

POSITIVE = 1
NEGATIVE = 0
dataList = []

def build_data_frame(tweet_filename,data):
    data_frame = DataFrame({'text': [], 'class': []})
    reader = tsv.TsvReader(open(tweet_filename))
    #input_tweet = open(tweet_filename, 'r')
    count = 0
    for line in reader:
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
    

    data = data.append(data_frame)
    
    dataList.append(data_frame)

    return data_frame

def main():
    print "starting"
    args = list(sys.argv)
    tweet_filename = args[1]
    out_file = open('tweet_classifier_bigrams.output','w')

    team_files = glob.glob(args[2] + '/*')

    data = DataFrame({'text': [], 'class': []})

    
    threads = []
    
    for i in range(10):
        
        fileName = "partition"+str(i)+".txt"
        #build_data_frame(fileName,data)
        threads.append(threading.Thread(target=build_data_frame, args=(fileName,data)))
    print "threads"    
    for i in range(10):
        threads[i].start()
        print "started thread "+str(i)
    for i in range(10):
        threads[i].join()
        print "ended thread "+str(i)


    print "threads done?"
    print len(dataList)
    for i in range(10):
        data = data.append(dataList[i])


    #  data = data.reindex(numpy.random.permutation(data.index))
    print "about to do vectorization"
    count_vectorizer = CountVectorizer(ngram_range=(1, 2))
    #count_vectorizer = CountVectorizer()
    print data
    counts = count_vectorizer.fit_transform(numpy.asarray(data['text']))
    classifier = MultinomialNB()
    targets = numpy.asarray(data['class'])
    classifier.fit(counts, targets)
    correct_count = 0

    print "bring classifying"
    examples = list()

    scores = {}

    for f in team_files:
        team = f[4:-10]  # <-- the next hot emoticon??? 6roundbreaking

        test = tsv.TsvReader(open(f))
        class_count = {'positive': 0, 'negative': 0}
        total_test = 0

        for tweet in test:
            #tweet = tweet.split('    ')
            #tweet_class = tweet[1]
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

            class_count[class_result] += 1
            total_test += 1

            examples.pop()
            # output to file
            #tweet_content = ' '.join(tweet_content)
        pos_percentage = 100*(float(class_count['positive']) / float(total_test))
        neg_percentage = 100*(float(class_count['negative']) / float(total_test))
        scores[team] = {'positive': pos_percentage, 'negative': neg_percentage}

    for team in sorted(scores, key=scores.get('positive'), reverse=True):
        out_file.write(team + '\t' + '{0:.2f}%'.format(scores[team]['positive']) + ' positive and ' + '{0:.2f}%'.format(scores[team]['negative']) + ' negative\n')


if __name__  == "__main__":
    main()
