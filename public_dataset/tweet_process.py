# emojis -> words

import re
from porterstem import PorterStemmer
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

# Stems the lsit of tokens
def stemWords(tokens):
    stemmer = PorterStemmer()
    temp_tokens = []
    for token in tokens:
        token = stemmer.stem(token, 0, len(token)-1)
        temp_tokens.append(token)

    return temp_tokens

# Removes stopwords from tokens list
def removeStopwords(tokens):
    updated_tokens = []

    # load stopwords
    stopwords = set(line.strip().lower() for line in open('stopwords'))

    for token in tokens:
        # check for empty empty line
        if len(token) == 0:
            continue
        # remove stopwords
        if token in stopwords:
            continue
        updated_tokens.append(token)
    
    return updated_tokens

# Helper function to tokenize commass
def tokenize_commas(tokens):

    temp_tokens = []
    for token in tokens:
        start_pos = 0
        index = token.find(',', start_pos)
        # loop until have checked every ,
        # remove unnecesary , 's 
        while(index != -1):
            start_pos = index
            if index == 0:
                token = token[1:]
            elif index == len(token)-1:
                token = token[:len(token)-1]
            elif not token[index-1:index].isdigit() or not token[index+1:index+2].isdigit():
                token = token[:index] + token[index+1:]
            else:
                start_pos = start_pos + 1
            index = token.find(',', start_pos)

        # check for now empty strings
        if token:
            temp_tokens.append(token)

    return temp_tokens

# Helper function to tokenize dashes
def tokenize_dashes(tokens):

    temp_tokens = []
    for token in tokens:
        start_pos = 0
        index = token.find('-', start_pos)
        # loop until have checked every -
        # remove dashes that are not indicative of a pharse i.e. state-of-the-art
        while(index != -1):
            start_pos = index
            if index == 0:
                token = token[1:]
            elif index == len(token)-1:
                token = token[:len(token)-1]
            elif not token[index-1:index].isalnum() or not token[index+1:index+2].isalnum():
                token = token[:index] + token[index+1:]
            else:
                start_pos = start_pos + 1
            index = token.find('-', start_pos)

        # check for empty strings
        if token:
            temp_tokens.append(token)

    return temp_tokens

# helper function to create dict of contractions from contract file
def getContractions():

    contract_dict = {}
    # read each line 
    with open ("contractions.txt", "r") as doc:
        for line in doc:
            line = line.strip().lower()
            split_line = line.split(' ', 1)
            contract_dict[split_line[0]] = split_line[1]

    return contract_dict

# helper function to tokenize apostrophes
def tokenize_apostrophes(content):

    contractions_dict = getContractions()
    tokens = []
    for token in content.split():
        if token in contractions_dict:
            tokens += contractions_dict[token].split()
        else:
            # find all apostrophes and eliminate or seperate if possessive
            start_pos = 0
            index = token.find('\'', start_pos)

            # loop until have checked every apostrophe
            # remove unnecesary apostrophes
            while(index != -1):
                start_pos = index
                if index == 0:
                    token = token[1:]
                elif index == len(token)-1:
                    token = token[:len(token)-1]
                elif index == len(token) -2 and token[index + 1] == 's':
                    token = token[:index]
                    tokens.append("'s")
                else:
                    token = token[:index] + token[index+1:]

                index = token.find('\'', start_pos)

            # check for now empty strings
            if token:
                tokens.append(token)

    # print tokens
    return tokens 

def tweet_process(tweet_string):
    tweet = tokenize_apostrophes(tweet_string)
    tweet = delete_duplicates(tweet)
    tweet = delete_mentions(tweet)
    tweet = delete_urls(tweet)
    tweet = removeStopwords(tweet)
    tweet = tokenize_dashes(tweet)
    tweet = tokenize_commas(tweet)
    tweet = stemWords(tweet)
    return remove_hashtags(tweet)
