# -*- coding: utf-8 -*- 
"""
fr = open("d2.txt")
a = ""
for line in fr:
	a = a+" "+line.strip()

print len(a)
fw = open("d22.txt","w")
fw.write(a)
"""



def getPureWord(w):
    temp = w.lower().strip()

    #number and word
    #print ''.join(e for e in temp if e.isalnum())        
    temp = ''.join(e for e in temp if e.isalpha()) 
    return temp

line = open("dict.txt").read()
s = set()
for w in line.split():
	s.add(w.strip())
b = list(s)
fw = open("dict2.txt","w")
fw.write(" ".join(b))

