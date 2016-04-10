#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
usage:
	python random_baselining.py /file/to/input
	/file/to/input should be in .csv
"""
import math
import random
import sys
import operator
import os
import time
col_beg = 7
col_end = 12
fn = sys.argv[1]

def randArray(length):
	return [str(random.randint(0,1)) for _ in xrange(length)]
def mergeArray(line):
	words = line.split(',')
	op = []
	a = randArray(col_end-col_beg+1)
	op.extend(words[0:col_beg-1])
	op.extend(a)
	op.extend(words[col_end])
	return ",".join(op)


def randomB(fn):
	fw = open(fn[-4]+"_random.csv","w")
	fr = open(fn,"r")
	for line in fr:
		op = mergeArray(line)
		fw.write(op)
		fw.write("\n")
	fw.close
	fr.close

if os.path.exists(fn):
	if fn.endswith(".csv"):
		randomB(fn)
	else:
		print "File should end with .csv"

else:
    print "File does not exists"




