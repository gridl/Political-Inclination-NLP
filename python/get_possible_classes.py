#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import math
import random
import sys
import operator
import os
import time
fn = sys.argv[1]
data_column = int(sys.argv[1])
classify = {}
def buildHash():
	"Hillary, Bernie, Trump, Cruz, GOP, DEM"	
	classify["trump"] = ["donald","trump"]
	classify["cruz"] = []
	classify["hillary"] = []
	classify["bernie"] = []
	classify["gop"] = []
	classify["dem"] = []

def extendHash(key,entries):
	temp = entries
	if type(entries) != type(list("")):
		temp = type(entries)
	classify[key] = classify.get(key,[]).extend(temp)


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




