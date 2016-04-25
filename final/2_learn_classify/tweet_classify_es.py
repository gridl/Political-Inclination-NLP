# -*- coding: utf-8 -*-

import nltk
import csv
import random
import codecs
import re
from nltk.corpus import stopwords
import sys

# Declaring Global Variables
stopset = list(set(stopwords.words('spanish')))
hil_tweets = []
trump_tweets = []
bernie_tweets = []
cruz_tweets = []
classes = {}

# Transforming short forms into appropriate words
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
    return temp

# Removing http reference
def getPureWord(word):
    temp = word.lower()
    if str.startswith(temp,"http"):
        return ""
    temp = ''.join(e for e in temp if e.isalpha()) 
    if temp not in stopset and temp !='':
        return transform(temp)
    else:
        return ""

# Removing special characters
def purifyText(input):
    output = input.replace('\r','').replace('\n','')
    op = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', output)
    op1 = " ".join(getPureWord(w) for w in op.split())
    return op1.strip()
    #return input


# Building an entity hash of all candidates with their different mentions in tweets
def buildHash():
    #Hillary, Bernie, Trump, Cruz, GOP, DEM 
    classes["trump"] = ["donald","trump","donaldtrump"]
    classes["cruz"] = ["tedcruz","cruz","ted"]
    classes["hillary"] = ["hillaryclinton","hillary","clinton"]
    classes["bernie"] = ["berniesanders","bernie","sanders","bern"]
    classes["gop"] = ["gop","gopdebate","republicans"]
    classes["dem"] = ["dem","demdebate","democrats","Democratic","democrata","democrat"]


# Check whether the tweet mentions about any candidate(s)
def getEntities(line):
    line = line.lower()
    op = set()
    for key in classes:
        temp = classes[key]
        for t in temp:
            if t.lower() in line:
                op.add(key)
            if key in op:
                break
    return list(op)


# Filter out stop words and returns a dictionary input to the NLTK classifier
def tweet_word(words):
    return dict([(word.decode('utf-8'), True) for word in words.split() if word.decode('utf-8') not in stopset])


# Returns NLTK's Naive Bayes Classifier 
def getNaiveBayesClassifier(train_set):
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier


# Returns MEM's Naive Bayes Classifier
def getMemClassifier(train_set):
    # Ref - http://www.nltk.org/api/nltk.classify.html
    # ALGORITHMS = ['GIS', 'IIS', 'MEGAM', 'TADM']
    algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[1]
    classifier = nltk.MaxentClassifier.train(train_set, algorithm, max_iter=3)
    classifier.show_most_informative_features(10)
    return classifier


# The main function
def main():

    # Building Hash
    buildHash()

    # Declaring a test set
    test_set = []

    # Iterating over the annotated tweets and dividing them based on candidates
    for x in ['annotated.csv']:
        tweets = []
        with open('./' + x, 'rb') as csvfile:
            tweets = csvfile.readlines()
        for tweetstr in tweets:
            tweet = tweetstr.split(",")

            # Print if any error and exit
            if len(tweet) != 15:
                print tweet
                sys.exit()

            if tweet[13] == 'berniePositive':
                bernie_tweets.append(tweet)
            elif tweet[13] == 'hillaryPositive':
                hil_tweets.append(tweet)
            elif tweet[13] == 'cruzPositive':
                cruz_tweets.append(tweet)
            elif tweet[13] == 'trumpPositive':
                trump_tweets.append(tweet)
            elif "Negative" not in tweet[13]:
                test_set.append(tweet)


    # Shuffling them for randomness
    random.shuffle(bernie_tweets)
    random.shuffle(hil_tweets)
    random.shuffle(cruz_tweets)
    random.shuffle(trump_tweets)

    # Taking first 3000 tweets as the training data
    tr_bernie_tweets = bernie_tweets[:3000]
    tr_hil_tweets = hil_tweets[:3000]
    tr_cruz_tweets = cruz_tweets[:3000]
    tr_trump_tweets = trump_tweets[:3000]

    # All but first 3000 is our test data
    te_bernie_tweets = bernie_tweets[3000:]
    te_hil_tweets = hil_tweets[3000:]
    te_cruz_tweets = cruz_tweets[3000:]
    te_trump_tweets = trump_tweets[3000:]

    # Preparing the Training set as per the format of NLTK and removing stop words if any
    labeled_words = ([(purifyText(word[14]), 'hillaryPositive') for word in tr_hil_tweets] + [(purifyText(word[14]), 'trumpPositive') for word in tr_trump_tweets] + [(purifyText(word[14]), 'cruzPositive') for word in tr_cruz_tweets] + [(purifyText(word[14]), 'berniePositive') for word in tr_bernie_tweets])
    random.shuffle(labeled_words)
    featuresets = [(tweet_word(n), classify) for (n, classify) in labeled_words]
    train_set = featuresets


    # Uncomment this line if you don't need neutral tags
    #test_set = []

    # Adding all the remaining tweets to test set
    test_set.extend(te_bernie_tweets)
    test_set.extend(te_cruz_tweets)
    test_set.extend(te_trump_tweets)
    test_set.extend(te_hil_tweets)

    
    # Naive Bayes Classifier
    #classifier = getNaiveBayesClassifier(train_set)

    # MEM Classifier
    classifier = getMemClassifier(train_set)

    # Classifying and writing the results to file
    with open("classifyoutput.csv", 'wb') as f:
        
        # Check for randomness (This accuracy comes down 25% approx)
        random_tags = ["hillaryPositive", "trumpPositive", "cruzPositive", "berniePositive"]
        
        for tweet in test_set:
            random.shuffle(random_tags)

            # Purifying tweet from test set
            op1 = purifyText(tweet[14])
            
            # Checking if there are any candidate(s) is/are mentioned in the tweet
            op = getEntities(op1)

            # Classifying the tweet
            result = classifier.classify(tweet_word(op1))

            # If no entities found, assign a random tag
            # Else, shuffle the list 2 times and get the first candidate
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
            tweet.insert(14, result)
            
            # Writing all to file
            f.write(','.join(map(str, tweet)))
            f.write("\n")


# This is where all begins
if __name__ == "__main__":
    main()

