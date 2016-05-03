# -*- coding: utf-8 -*-

import nltk
import csv
import random
import codecs
import re
from nltk.corpus import stopwords

stopset = list(set(stopwords.words('spanish')))
pos_tweets = []
neg_tweets = []


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


# Process Tweet
def processTweet(tweet):
    tweet = tweet.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')
    return tweet


def tweet_word(words):
    return dict([(word.decode('utf-8'), True) for word in words.split() if word.decode('utf-8') not in stopset])


with codecs.open('../python/annotated_partaf', 'rb') as csvfile:
	tweets = csv.reader(csvfile, delimiter=',', quotechar='\'')
	for tweet in tweets:
		#print tweet
		#print tweet[11]
		if tweet[5] == '1':
			pos_tweets.append(processTweet(tweet[11]))
		elif tweet[5] == '-1':
			neg_tweets.append(processTweet(tweet[11]))


labeled_words = ([(word, 'positive') for word in pos_tweets] + [(word, 'negative') for word in neg_tweets])
random.shuffle(labeled_words)

featuresets = [(tweet_word(n), classify) for (n, classify) in labeled_words]

#print featuresets

train_set, test_set = featuresets[len(featuresets)/2:], featuresets[:len(featuresets)/2]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print train_set

testr = 'Éste naco pendejo no sabe ni comer pizza, cómo vergas va a saber gobernar un país'

#print classifier.classify(tweet_word(testr))
print(nltk.classify.accuracy(classifier, test_set))