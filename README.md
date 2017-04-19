# eecs486
Joel Battsek (jbattsek) Benjamin Foster (befost) Ashwin Fujii (afujii) Katherine Kampf (kkampf)

# File overview:
-NFL/ directory of .txt files continaing 1000 scraped tweets per each NFL team
-TweetScraper/ modified MIT Tweet Scraper used when Twitter API hit request limits
-all_tweets.txt hand annotated tweets for NFL teams
-download_tweets.py file to download public dataset tweets
-format_tweets.py helper file to reformat tweets when needed
-get_tweets.py file to grab tweets for all 32 NFL teams to then be hand annotated
-model_tweets.py file to train xgboost and svm classifiers using sklearn library
-naivebayes_test.py unigram naivebayes classifier
naivebayes_unigrams.py unigram anivebayes classifier to classify NFL/
-naivebayes_bigrams_threaded.py bigram naivebayes implementation using a threaded approach for maximum efficeny, includes both classifying NFL/ and test for accuracy on all_tweets/txt
-parseCSV.py helper to parse public dataset csv
-partitions/ partitioned files containing training tweets from the Sentiment 140 dataset
-s140_tweets.txt positive and negative training tweets from the Sentiment 140 dataset
-slang_words.txt text file with common abbreviations and their relatie expansions
-tweet_scraper.py file to gather NFL tweets from the Twitter API and confirm whether or not the tweets were made by a fan (meaning the have to follow the team they're tweeting about_
-tweet_process.py tweet preprocessing file
-utfer.py helper to eliminate s140 tweets that were causing utf encoding/decoding issues
-old/ old versions of files that are sometimes needed
-public_dataset/
    -final_datset UMICH SI650 - Sentiment Classification Training Data https://inclass.kaggle.com/c/si650winter11
        -small subset used for quick testing
    -tweeti-a.dist.tsv Sentiment 140 large dataset of classified tweets

# Running instructions:
-naivebayes_bigrams_threaded.py
    -run as `python naivebayes_bigrams_threaded.py anything NFL`
    -will train on partitions/ and test on all_tweets.txt for accuracy
    -Note: very very computationally heavy, takes forever to run

-naivebayes_unigrams.py
    -run as `python naiivebayes_unigrams.py training_filename NFL`
    -classifies NFL/ tweets

-naivebayes_test.py
    -run as `python naivebayes_test.py training_file`
    -modify NUM in main according to desired training/test split
