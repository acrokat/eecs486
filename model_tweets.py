import numpy as np
import string
import pickle
import sklearn
import tweet_process
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer

# Train and test XGBoost/SVM Classifier

def load_data(fname):
    tweetText = []
    tweetClass = []
    f = open(fname, 'r')
    for line in f.readlines():
        split_line = line.split('\t')
        tweetText.append(split_line[0].strip())
        tweetClass.append(2 if split_line[1].strip() == 'positive' else 1)
    return (tweetText, np.array(tweetClass))

def load_data_test(fname):
    tweetText = []
    tweetClass = []
    f = open(fname, 'r')
    for line in f.readlines():
        split_line = line.split('    ')
        tweetText.append(split_line[0].strip())
        tweetClass.append(2 if split_line[1].strip() == 'positive' else 1)
    return (tweetText, np.array(tweetClass))

def extract_dictionary(tweets):
    word_dict = {}
    word_index = 0
    tweets = tweet_process.tweet_process(tweets)
    for tweet in tweets:
        process_tweet = tweet.lower()
        for p in string.punctuation:
            process_tweet = process_tweet.replace(p, ' ' + p + ' ')
        for ngram in process_tweet.split():
            if ngram not in word_dict:
                word_dict[ngram] = word_index
                word_index += 1
    return word_dict

def extract_feature_vectors(tweets, word_list):
    feature_list = []
    for tweet in tweets:
        feature_vector = np.zeros((len(word_list),), dtype=np.int)
        for key in word_list:
            if key in tweet:
                feature_vector[word_list[key]] = 1
        feature_list.append(feature_vector)
    feature_matrix = np.vstack(feature_list)
    return feature_matrix

# Creating feature vectors
train_tweets = load_data('final_dataset')
train_tweet_list = train_tweets[0]
train_label_list = train_tweets[1]
print "loaded"
word_list = extract_dictionary(tweet_list)
feature_matrix = extract_feature_vectors(tweet_list, word_list)
print "extracted"

# Train XGBoost Classifier
xgb1 = xgb.XGBClassifier(
        learning_rate =0.1,
        n_estimators=200,
        max_depth=7,
        min_child_weight=1,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        objective= 'binary:logistic',
        nthread=4,
        scale_pos_weight=1,
        seed=27)
xgb1.fit(feature_matrix, label_list)

joblib.dump(xgb1, 'xgb.pkl', compress=1)
#xgb1 = joblib.load('xgb.pkl')

test_tweets = load_data_test('all_tweets.txt')
test_tweet_list = test_tweets[0]
test_label_list = test_tweets[1]
test_feature_matrix = extract_feature_vectors(test_tweet_list, word_list)
print "score:", metrics.accuracy_score(test_label_list, xgb1.predict(test_feature_matrix))

"""
# Tuning Code
x_list = [1]
y_list = [1]
for x in x_list:
    for y in y_list:
        xgb = xgb.XGBClassifier(
                learning_rate =0.1,
                n_estimators=200,
                max_depth=7,
                min_child_weight=1,
                gamma=0,
                subsample=0.8,
                colsample_bytree=0.8,
                objective= 'binary:logistic',
                nthread=4,
                scale_pos_weight=1,
                seed=27)
        print "cross validation"
        scores = cross_val_score(xgb, feature_matrix, label_list, cv=5)
        print x, y, np.average(scores)
"""
