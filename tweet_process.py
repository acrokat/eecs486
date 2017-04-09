# emojis -> words

import re

# input: list of tweet tokens

def delete_duplicates(tweet):
    return [re.sub(r'(.)\1+', r'\1\1', word) for word in tweet]

def delete_mentions(tweet):
    return [word for word in tweet if word[0] is not '@']

def delete_urls(tweet):
    return [word for word in tweet if 'http' not in word]

def remove_hashtags(tweet):
    for i, word in enumerate(tweet):
        if '#' in word:
            tweet[i] = word[1:]
    return tweet

def tweet_process(tweet):
    tweet = delete_duplicates(tweet)
    tweet = delete_mentions(tweet)
    tweet = delete_urls(tweet)
    return remove_hashtags(tweet)
