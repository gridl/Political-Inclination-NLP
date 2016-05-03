# -*- coding: utf-8 -*-

import nltk
import csv
import random
import codecs
from nltk.corpus import stopwords

stopset = list(set(stopwords.words('spanish')))
pos_tweets = []
neg_tweets = []


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def tweet_word(words):
    return dict([(word.decode('utf-8'), True) for word in words.split() if word.decode('utf-8') not in stopset])


reader = unicode_csv_reader(open('testmodel/trump_es.csv'))

with codecs.open('testmodel/trump_es.csv', 'rb') as csvfile:
	tweets = csv.reader(csvfile, delimiter=',', quotechar='\'')
	for tweet in tweets:
		if tweet[0] == '1':
			pos_tweets.append(tweet[1])
		else:
			neg_tweets.append(tweet[1])


labeled_words = ([(word, 'positive') for word in pos_tweets] + [(word, 'negative') for word in neg_tweets])
random.shuffle(labeled_words)

featuresets = [(tweet_word(n), classify) for (n, classify) in labeled_words]

#print featuresets

train_set, test_set = featuresets[5:], featuresets[:5]
classifier = nltk.NaiveBayesClassifier.train(train_set)

testr = 'Éste naco pendejo no sabe ni comer pizza, cómo vergas va a saber gobernar un país'

print classifier.classify(tweet_word(testr))
