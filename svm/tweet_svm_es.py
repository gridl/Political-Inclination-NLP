# -*- coding: utf-8 -*-

import csv
import random
import codecs
import re
#from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier #SVM Linear


#stopset = list(set(stopwords.words('spanish')))
stopwords = ["rt","un","una","unas","unos","uno","sobre","todo","también","tras","otro","algún","alguno","alguna","algunos","algunas","ser","es","soy","eres","somos","sois","estoy","esta","estamos","estais","estan","como","en","para","atras","porque","por qué","estado","estaba","ante","antes","siendo","ambos","pero","por","poder","puede","puedo","podemos","podeis","pueden","fui","fue","fuimos","fueron","hacer","hago","hace","hacemos","haceis","hacen","cada","fin","incluso","primero desde","conseguir","consigo","consigue","consigues","conseguimos","consiguen","ir","voy","va","vamos","vais","van","vaya","gueno","ha","tener","tengo","tiene","tenemos","teneis","tienen","el","la","lo","las","los","su","aqui","mio","tuyo","ellos","ellas","nos","nosotros","vosotros","vosotras","si","dentro","solo","solamente","saber","sabes","sabe","sabemos","sabeis","saben","ultimo","largo","bastante","haces","muchos","aquellos","aquellas","sus","entonces","tiempo","verdad","verdadero","verdadera   cierto","ciertos","cierta","ciertas","intentar","intento","intenta","intentas","intentamos","intentais","intentan","dos","bajo","arriba","encima","usar","uso","usas","usa","usamos","usais","usan","emplear","empleo","empleas","emplean","ampleamos","empleais","valor","muy","era","eras","eramos","eran","modo","bien","cual","cuando","donde","mientras","quien","con","entre","sin","trabajo","trabajar","trabajas","trabaja","trabajamos","trabajais","trabajan","podria","podrias","podriamos","podrian","podriais","yo","aquel"]
stopset = list(set(stopwords))
pos_tweets = []
neg_tweets = []
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

train_tags = []
train_tweets = []

#for x in ['a', 'b', 'c', 'd', 'e', 'f']:
for x in ['annotatedTrump2.csv']:
    with codecs.open('../python/annotated2/' + x, 'rb') as csvfile:
        tweets = csv.reader(csvfile, delimiter=',', quotechar='\'')
        for tweet in tweets:
            if tweet[7] == '1':
    			train_tags.append(0)
            elif tweet[7] == '-1':
                train_tags.append(1)
            train_tweets.append(purifyText(tweet[13]))

text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),])
text_clf = text_clf.fit(train_tweets, train_tags)

# Generating Test Set...
for x in ['testTrump.csv']:
    with codecs.open('../python/annotated2/' + x, 'rb') as csvfile:
        tweets = csv.reader(csvfile, delimiter=',', quotechar='\'')
        for tweet in tweets:
            if tweet[7] == '0':
                test_set.append(tweet)

i = 1
with open("svmoutput.csv", 'wb') as f:
    for tweet in test_set:
        op1 = purifyText(tweet[13])
        op = getEntities(op1)
        if "trump" in op:
            result = text_clf.predict([op1])
            if result[0] == 0:
                tweet[7] = 1
                tweet[12] = tweet[12] + "/positive"
            else:
                tweet[7] = -1
                tweet[12] = tweet[12] + "/negative"

            f.write(','.join(map(str, tweet)))
            f.write("\n")
