import sys
import os
input_tweets = set()
compare_tweets = set()
fn = sys.argv[1]
data_column= 12
filelist = ["annotated2/annotated.csv.sortedaa","annotated2/annotated.csv.sortedab","annotated2/annotated.csv.sortedac","annotated2/annotated.csv.sortedad","annotated2/annotated.csv.sortedae","annotated2/annotated.csv.sortedaf"]
def readCompare():
	for file in filelist:
		fr = open(file,"r")
		for line in 