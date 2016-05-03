This project contains two folders:-
Experimental : This folder contains all the source codes used for development of the project. This also includes the source codes not part of the final project

Final Project Codes : This folder is the final set of source codes we used for implementation and code demonstration.
- 1_retrival
	- twitter_extraction.py : This code extracts tweets in Spanish using keywords which are viral for Presidential primary elections 2016.
	- annotate.py : This is an automatic annotator script which takes the raw extracted data as input and tags some of the corpus with their correct sentiment.
- 2_learn_classify
	- tweet_classify_es.py : This code implements the classification system using NLTK's NB and MEM. While classifying the data, we are also marking them using Improvised baseline mechanism as discussed in the report.
	- tweet_classify_es.py : This code implements the classification system using scikit learn's SVM.
