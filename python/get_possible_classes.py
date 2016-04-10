#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""
usage:
	python get_possible_classes.py /file/to/input data_column
	/file/to/input should be in .csv
	just add any entries which identifies the classes. list is case insensitive
"""
import math
import random
import sys
import operator
import os
import time
import re
fn = sys.argv[1]
data_column = int(sys.argv[2])
classify = {}

spanish_stop_words = ["rt","un","una","unas","unos","uno","sobre","todo","también","tras","otro","algún","alguno","alguna","algunos","algunas","ser","es","soy","eres","somos","sois","estoy","esta","estamos","estais","estan","como","en","para","atras","porque","por qué","estado","estaba","ante","antes","siendo","ambos","pero","por","poder","puede","puedo","podemos","podeis","pueden","fui","fue","fuimos","fueron","hacer","hago","hace","hacemos","haceis","hacen","cada","fin","incluso","primero	desde","conseguir","consigo","consigue","consigues","conseguimos","consiguen","ir","voy","va","vamos","vais","van","vaya","gueno","ha","tener","tengo","tiene","tenemos","teneis","tienen","el","la","lo","las","los","su","aqui","mio","tuyo","ellos","ellas","nos","nosotros","vosotros","vosotras","si","dentro","solo","solamente","saber","sabes","sabe","sabemos","sabeis","saben","ultimo","largo","bastante","haces","muchos","aquellos","aquellas","sus","entonces","tiempo","verdad","verdadero","verdadera	cierto","ciertos","cierta","ciertas","intentar","intento","intenta","intentas","intentamos","intentais","intentan","dos","bajo","arriba","encima","usar","uso","usas","usa","usamos","usais","usan","emplear","empleo","empleas","emplean","ampleamos","empleais","valor","muy","era","eras","eramos","eran","modo","bien","cual","cuando","donde","mientras","quien","con","entre","sin","trabajo","trabajar","trabajas","trabaja","trabajamos","trabajais","trabajan","podria","podrias","podriamos","podrian","podriais","yo","aquel"]
stop_words = ['the','be','and','an','i','he','it','is','of','in','or','was','he','she','av','aug','august','where','week','we','hors','wc','us','am','at','ci','my','nd','rri','sw','to','aaa','abd','ae','fl','im','its']
online_stop = ['a', 'able', 'about', 'above', 'abroad', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'adopted', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ago', 'ah', 'ahead', 'aint', 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'alongside', 'already', 'also', 'although', 'always', 'am', 'amid', 'amidst', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'apparently', 'appear', 'appreciate', 'appropriate', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'backward', 'backwards', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'best', 'better', 'between', 'beyond', 'bill', 'biol', 'both', 'bottom', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'call', 'came', 'can', 'cannot', 'cant', 'caption', 'cause', 'causes', 'certain', 'certainly', 'changes', 'clearly', 'cmon', 'co', 'co.', 'com', 'come', 'comes', 'computer', 'con', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could', 'couldnt', 'course', 'cry', 'cs', 'currently', 'd', 'dare', 'darent', 'date', 'de', 'definitely', 'describe', 'described', 'despite', 'detail', 'did', 'didnt', 'different', 'directly', 'do', 'does', 'doesnt', 'doing', 'done', 'dont', 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'end', 'ending', 'enough', 'entirely', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'evermore', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'f', 'fairly', 'far', 'farther', 'few', 'fewer', 'ff', 'fifteen', 'fifth', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'forever', 'former', 'formerly', 'forth', 'forty', 'forward', 'found', 'four', 'from', 'front', 'full', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'h', 'had', 'hadnt', 'half', 'happens', 'hardly', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hello', 'help', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herse', 'herself', 'hes', 'hi', 'hid', 'him', 'himse', 'himself', 'his', 'hither', 'home', 'hopefully', 'how', 'howbeit', 'however', 'hows', 'hundred', 'i', 'id', 'ie', 'if', 'ignored', 'ill', 'im', 'immediate', 'immediately', 'importance', 'important', 'in', 'inasmuch', 'inc', 'inc.', 'indeed', 'index', 'indicate', 'indicated', 'indicates', 'information', 'inner', 'inside', 'insofar', 'instead', 'interest', 'into', 'invention', 'inward', 'is', 'isnt', 'it', 'itd', 'itll', 'its', 'itse', 'itself', 'ive', 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'keys', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'likewise', 'line', 'little', 'll', 'look', 'looking', 'looks', 'low', 'lower', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'maynt', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'mightnt', 'mill', 'million', 'mine', 'minus', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'move', 'mr', 'mrs', 'much', 'mug', 'must', 'mustnt', 'my', 'myse', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'neednt', 'needs', 'neither', 'never', 'neverf', 'neverless', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'no-one', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'notwithstanding', 'novel', 'now', 'nowhere', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'opposite', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'oughtnt', 'our', 'ours', 'ours ', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'presumably', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provided', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'reasonably', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted', 'resulting', 'results', 'right', 'round', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'second', 'secondly', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', 'shant', 'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'show', 'showed', 'shown', 'showns', 'shows', 'side', 'significant', 'significantly', 'similar', 'similarly', 'since', 'sincere', 'six', 'sixty', 'slightly', 'so', 'some', 'somebody', 'someday', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'state', 'states', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure', 'system', 't', 'take', 'taken', 'taking', 'tell', 'ten', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', 'thatll', 'thats', 'thatve', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', 'therell', 'thereof', 'therere', 'theres', 'thereto', 'thereupon', 'thereve', 'these', 'they', 'theyd', 'theyll', 'theyre', 'theyve', 'thick', 'thin', 'thing', 'things', 'think', 'third', 'thirty', 'this', 'thorough', 'thoroughly', 'those', 'thou', 'though', 'thoughh', 'thousand', 'three', 'throug', 'through', 'throughout', 'thru', 'thus', 'til', 'till', 'tip', 'to', 'together', 'too', 'took', 'top', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'ts', 'twelve', 'twenty', 'twice', 'two', 'u', 'un', 'under', 'underneath', 'undoing', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'upwards', 'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'uucp', 'v', 'value', 'various', 've', 'versus', 'very', 'via', 'viz', 'vol', 'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'welcome', 'well', 'went', 'were', 'werent', 'weve', 'what', 'whatever', 'whatll', 'whats', 'whatve', 'when', 'whence', 'whenever', 'whens', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'whichever', 'while', 'whilst', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', 'wholl', 'whom', 'whomever', 'whos', 'whose', 'why', 'whys', 'widely', 'will', 'willing', 'wish', 'with', 'within', 'without', 'wonder', 'wont', 'words', 'world', 'would', 'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', 'youll', 'your', 'youre', 'yours', 'yourself', 'yourselves', 'youve', 'z', 'zero']
stop_words.extend(online_stop)
stop_words.extend(spanish_stop_words)

stop_words = list(set(stop_words))


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
    #	return ""
    #print word
    temp = word.lower()
    if str.startswith(temp,"http"):
        return ""
    temp = ''.join(e for e in temp if e.isalpha()) 
    if temp not in stop_words and temp !='':
        return transform(temp)
    else:
        return ""

def purifyText(input):
	
	output = input.replace('\r','').replace('\n','')
	op = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', output)
	op1 = " ".join(getPureWord(w) for w in op.split())
	#print op1
	return op1.strip()


def buildHash():
	#Hillary, Bernie, Trump, Cruz, GOP, DEM	
	classify["trump"] = ["donald","trump","donaldtrump"]
	classify["cruz"] = ["tedcruz","cruz","ted"]
	classify["hillary"] = ["hillaryclinton","hillary","clinton"]
	classify["bernie"] = ["berniesanders","bernie","sanders","bern"]
	classify["gop"] = ["gop","gopdebate","republicans"]
	classify["dem"] = ["dem","demdebate","democrats","Democratic","democrata","democrat"]

def extendHash(key,entries):
	temp = entries
	if type(entries) != type(list("")):
		temp = type(entries)
	classify[key] = classify.get(key,[]).extend(temp)

def getEntities(line):
	line = line.lower()
	op = set()
	for key in classify:
		temp = classify[key]
		for t in temp:
			#print type(line)
			if t.lower() in line:
				op.add(key)
			if key in op:
				break
	return list(op)


def getCl(fn):
	fr = open(fn,"r")
	for l in fr:
		line = purifyText(l.split(",")[data_column-1])
		op = getEntities(line)
		if "dem" in op and "bernie" not in op:
			print op
			print line
			print l.split(",")[data_column-1]
			print "\n"
	fr.close

if os.path.exists(fn):
	if fn.endswith(".csv"):
		buildHash()
		getCl(fn)
	else:
		print "File should end with .csv"
else:
    print "File does not exists"




