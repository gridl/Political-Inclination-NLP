# Analyzing Political Inclination of Twitter Users
CSCI-544 Final Project - House of Translators(HoT)

# Introduction
The United States Presidential Elections take place every four years with new (sometimes old) candidates every time from the two major political parties, namely Republican and Democratic. We have analyzed Twitter user’s political inclination towards Presidential candidates. We employed three different techniques namely Naïve Bayes (NB), MEMs (Maximum Entropy Models) and SVMs (Support Vector Machines) and compared their results. These techniques can also be used for the analysis of future elections and also for other languages by changing a few input and classification parameters.

## Usage
The final set of source codes used for implementation and code demonstration is in *Final-Project-Codes* folder.

**1_retrival**

`twitter_extraction.py` : This code extracts tweets in Spanish using keywords which are viral for Presidential primary elections 2016.
  > python twitter_extraction.py 

`annotate.py` : This is an automatic annotator script which takes the raw extracted data as input and tags some of the corpus with their correct sentiment.
  > python annotate.py [path_to_file]

**2_learn_classify**

`tweet_classify_es.py`: This code implements the classification system using NLTK's NB and MEM models.
  > For using NB model:-
  
  > python tweet_classify_es.py nb [path_to_file]
  
  > For using MEM model:-
  
  > python tweet_classify_es.py mem [path_to_file]
  
`tweet_svm_classify_es.py`: This code implements the classification system using scikit learn's SVM.
  > python tweet_svm_classify_es.py [path_to_file]

# Contributions
1. [Nishant Kakar](https://github.com/nishantkakar)
2. [Karanjeet Singh](https://github.com/karanjeets)
3. [Abhishek Patro](https://github.com/agbpatro)
4. [Pawan Valluri](https://github.com/pawanvalluri)
