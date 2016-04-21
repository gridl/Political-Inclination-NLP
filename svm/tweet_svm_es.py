# -*- coding: utf-8 -*-

import nltk
import csv
import random
import codecs
import re
from nltk.corpus import stopwords
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier #SVM Linear

stopset = list(set(stopwords.words('spanish')))
hil_tweets = []
trump_tweets = []
bernie_tweets = []
cruz_tweets = []
classes = {}

def transform(temp):
    if temp == "imo":
        return "opinion"
    elif temp == "inches":
        return "inch"
    elif temp == "including" or temp == "included" or temp == "includes":
        return "include"
    elif temp == "issued" or temp == "issues":
        return "issue"
    elif temp == "ppl":
        return "people"
    elif temp == "prices":
        return "price"
    elif temp == "say":
        return "says"
    elif temp == "shocked" or temp == "shocker" or temp == "shocking":
        return "shock"
    #elif temp == "sooooo" or temp == "soooo" or temp == "sooo" or temp == "soo":
    #    return "so"
    return temp

def getPureWord(word):
    #if str.startswith(word,'@'):
    #   return ""
    #print word
    temp = word.lower()
    if str.startswith(temp,"http"):
        return ""
    temp = ''.join(e for e in temp if e.isalpha()) 
    #if temp not in stop_words and temp !='':
    if temp not in stopset and temp !='':
        return transform(temp)
    else:
        return ""

def purifyText(input):
    output = input.replace('\r','').replace('\n','')
    op = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', output)
    op1 = " ".join(getPureWord(w) for w in op.split())
    return op1.strip()
    #return input


def buildHash():
    #Hillary, Bernie, Trump, Cruz, GOP, DEM 
    classes["trump"] = ["donald","trump","donaldtrump"]
    classes["cruz"] = ["tedcruz","cruz","ted"]
    classes["hillary"] = ["hillaryclinton","hillary","clinton"]
    classes["bernie"] = ["berniesanders","bernie","sanders","bern"]
    classes["gop"] = ["gop","gopdebate","republicans"]
    classes["dem"] = ["dem","demdebate","democrats","Democratic","democrata","democrat"]


def getEntities(line):
    line = line.lower()
    op = set()
    for key in classes:
        temp = classes[key]
        #print temp
        for t in temp:
            #print type(line)
            if t.lower() in line:
                op.add(key)
            if key in op:
                break
    return list(op)


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


buildHash()
test_set = []

#for x in ['a', 'b', 'c', 'd', 'e']:
for x in ['annotated.csv']:
    #with codecs.open('../python/Annotated4/annotated.csva' + x, 'rb') as csvfile:
    tweets = []
    with open('./' + x, 'rb') as csvfile:
        tweets = csvfile.readlines()
        #tweets = csv.reader(csvfile, delimiter=',')
        #random.shuffle(tweets)
    for tweetstr in tweets:
        tweet = tweetstr.split(",")
        if len(tweet) != 15:
            print tweet
            sys.exit()
        #print tweet[13]
        #sys.exit()
        if tweet[13] == 'berniePositive':
            bernie_tweets.append(tweet)
        elif tweet[13] == 'hillaryPositive':
            hil_tweets.append(tweet)
        elif tweet[13] == 'cruzPositive':
            cruz_tweets.append(tweet)
        elif tweet[13] == 'trumpPositive':
            trump_tweets.append(tweet)
        #elif tweet[12] == 'nuetral':
        #    test_set.append(tweet)



random.shuffle(bernie_tweets)
random.shuffle(hil_tweets)
random.shuffle(cruz_tweets)
random.shuffle(trump_tweets)

tr_bernie_tweets = bernie_tweets[:3000]
tr_hil_tweets = hil_tweets[:3000]
tr_cruz_tweets = cruz_tweets[:3000]
tr_trump_tweets = trump_tweets[:3000]

te_bernie_tweets = bernie_tweets[3000:]
te_hil_tweets = hil_tweets[3000:]
te_cruz_tweets = cruz_tweets[3000:]
te_trump_tweets = trump_tweets[3000:]

#labeled_words = ([(purifyText(word[14]), 'hillaryPositive') for word in tr_hil_tweets] + [(purifyText(word[14]), 'trumpPositive') for word in tr_trump_tweets] + [(purifyText(word[14]), 'cruzPositive') for word in tr_cruz_tweets] + [(purifyText(word[14]), 'berniePositive') for word in tr_bernie_tweets])
train_tweets = [purifyText(word[14]) for word in tr_hil_tweets] + [purifyText(word[14]) for word in tr_trump_tweets] + [purifyText(word[14]) for word in tr_cruz_tweets] + [purifyText(word[14]) for word in tr_bernie_tweets]
train_tags = ([0]*3000) + ([1]*3000) + ([2]*3000) + ([3]*3000)

text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),])
text_clf = text_clf.fit(train_tweets, train_tags)

#random.shuffle(labeled_words)
#featuresets = [(tweet_word(n), classify) for (n, classify) in labeled_words]
#train_set = featuresets

'''
labeled_words = ([(word, 'hillary') for word in te_hil_tweets] + [(word, 'trump') for word in te_trump_tweets] + [(word, 'cruz') for word in te_cruz_tweets] + [(word, 'bernie') for word in te_bernie_tweets])
random.shuffle(labeled_words)
featuresets = [(tweet_word(n), classify) for (n, classify) in labeled_words]
test_set = featuresets
'''
# Generating Test Set...
'''
for x in ['testTrump.csv']:
    with codecs.open('../python/annotated2/' + x, 'rb') as csvfile:
        tweets = csv.reader(csvfile, delimiter=',', quotechar='\'')
        for tweet in tweets:
            if tweet[7] == '0':
                test_set.append(tweet)
'''

test_set = []
test_set.extend(te_bernie_tweets)
test_set.extend(te_cruz_tweets)
test_set.extend(te_trump_tweets)
test_set.extend(te_hil_tweets)

# Ref - http://www.nltk.org/api/nltk.classify.html
# ALGORITHMS = ['GIS', 'IIS', 'MEGAM', 'TADM']
#algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[1]
#classifier = nltk.MaxentClassifier.train(train_set, algorithm, max_iter=3)
#classifier.show_most_informative_features(10)

#classifier = nltk.NaiveBayesClassifier.train(train_set)

#print(nltk.classify.accuracy(classifier, test_set))


with open("classifyoutput.csv", 'wb') as f:
    random_tags = ["hillaryPositive", "trumpPositive", "cruzPositive", "berniePositive"]
    all_tags = ["hillaryPositive", "trumpPositive", "cruzPositive", "berniePositive"]
    for tweet in test_set:
        random.shuffle(random_tags)
        op1 = purifyText(tweet[14])
        
        op = getEntities(op1)

        #result = classifier.classify(tweet_word(op1))
        result = text_clf.predict([op1])
        #if result.strip() == "" or op1.strip() == "":
        #    print "Problem!!!! ",op1, result

        #print tweet[14], result

        if not op:
            tweet.insert(14, random_tags[0])
        else:
            random.shuffle(op)
            random.shuffle(op)

            if "trump" in op[0]:
                tweet.insert(14, "trumpPositive")
            elif "cruz" in op[0]:
                tweet.insert(14, "cruzPositive")
            elif "hillary" in op[0]:
                tweet.insert(14, "hillaryPositive")
            elif "bernie" in op[0]:
                tweet.insert(14, "berniePositive")
            else:
                tweet.insert(14, random_tags[0])

        tweet.insert(14, random_tags[0])
        tweet.insert(14, all_tags[result[0]])
        

        f.write(','.join(map(str, tweet)))
        f.write("\n")

        '''
        if "trump" in op or "bernie" in op or "hillary" in op or "cruz" in op:
            result = classifier.classify(tweet_word(op1))
            print tweet[13]
            print result
        '''
        #else:
        #    print result + "Positive"

