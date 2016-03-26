# -*- coding: utf-8 -*-

import nltk
import csv
import random
from nltk.corpus import stopwords

stopset = list(set(stopwords.words('english')))
pos_tweets = []
neg_tweets = []


def tweet_word(words):
    return dict([(word, True) for word in words.split() if word not in stopset])

with open('/Users/karanjeetsingh/git_workspace/csci544/classifier/testmodel/bernie.csv', 'rb') as csvfile:
	tweets = csv.reader(csvfile, delimiter=',', quotechar='\'')
	for tweet in tweets:
		if tweet[0] == '1':
			pos_tweets.append(tweet[1])
		else:
			neg_tweets.append(tweet[1])


labeled_words = ([(word, 'positive') for word in pos_tweets] + [(word, 'negative') for word in neg_tweets])
random.shuffle(labeled_words)

featuresets = [(tweet_word(n), classify) for (n, classify) in labeled_words]

print featuresets

train_set, test_set = featuresets[5:], featuresets[:5]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print classifier.classify(tweet_word('Bernie sanders is a mentally handicapped Jew with ties to Israel who supports the killing of babies but not of violent criminals'))
