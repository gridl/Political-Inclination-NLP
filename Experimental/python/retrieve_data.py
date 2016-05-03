import tweepy
import random
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import goslate
import sys
from translate import translator
import urllib2
import jsonpickle
reload(sys)
sys.setdefaultencoding("utf-8")


#consumer key, consumer secret, access token, access secret.

ckey="fsdfasdfsafsffa"
csecret="asdfsadfsadfsadf"
atoken="asdf-aassdfs"
asecret="asdfsadfsdafsdafs"
"""
consumer_key = 'BuamdDtGgiUMFjPX0j1ZGfFuU'
consumer_secret = 'r06YXs2wRePrsCMOdWWMxKBDUP7AEjZLmzcuxSNYHvuQB8ynXc'
access_token = '108324710-FNh5JrXEMMycUqKum5GSCKDjzYSGN0qhypGN1S4v'
access_secret = 'JIpQZ7z23NiQqtkFSR8GEEvaPPUlF44w9zB0tkvkU5JFY'

"""

consumer_key = 'kZyMSZBRORZaDdutIIMja6v85'
consumer_secret = 'Mbu2HqI0Ea6MSIRr3B7MKgMSxEdQpJXqOEb4n4oAMLLulQxDXm'
access_token = '84823887-ZAiJrvVV5WxmSiTnOUdya2ZzNjur7DCL4Xkyoia5r'
access_secret = '3Hf0OAKKtue0TPOcFkCcgK153eOKv4dCoqcQOAC1rzIMy'

"""
access_token="74693581-fOWOuGkCBKYyYWdHiCCIvmxB6V3aSry7LxhSojWiA"
access_secret="3YppAZgpqjGGhHg9XpQPaneKqYOvUiT6tz1ZAjwry5LNw"
consumer_key="HQNUFeGBA3vCuebSS2T51a7Wt"
consumer_secret="3NhJIU6J4aHpYbJlOyQ75Yjko4JGHBD4fgmwjAn1tlQ7duiPpe"


consumer_key = "BlweSNHSKmeSur5YkXMxzkUUV"
consumer_secret.extend = "KocCMLcrY4u34eqt2UNSm9wk89MZdrRSjKfZdzJxVgKNT56aCI"
access_token.extend = "4317032720-yxQUoRRj6SZtDSSf7RsgvSCjukEHFNbQGbWJPpY"
access_secret.extend = "UWRd46OzsWezffVASlQpzgJ8EMUcX2HHZPFadw4bM7K9k"

"""

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


proxy_handler = urllib2.ProxyHandler({"http" : "http://52.10.153.135:8083"})
proxy_opener = urllib2.build_opener(urllib2.HTTPHandler(proxy_handler),
                                    urllib2.HTTPSHandler(proxy_handler))

#gs = goslate.Goslate(opener=proxy_opener)
gs = goslate.Goslate()

t_list = [] 

searched_tweets = []
last_id = -1
max_tweets = 300000
individual_hash_level = max_tweets
q_tags = []
queryList1 = ["feelthebern","wewantbernie","stillsanders","presidentbernie","weendorsebernie","berniesanders2016","voteforberniesanders","vote4bernie","berniesanders","berniesandersforpresident","bernie2016","election2016","bernie","hillaryclinton","trump","hillary2016","tedcruz","republicans","cruz2016","imwithher","hillary","democrats","conservatives","donaldtrump","voteforbernie","cruz","trump2016","makeamericahateagain","drumpf","makedonalddrumpfagain","republican","trumptrain","gop","dumptrump","clinton2016","trumprally","presidentialelection","hilaryclinton","fuckhilary","fucktrump","mrtrump","letsmakeamericagreatagain","demdebate","gopdebate","trumpisachump","aipac2016","hillaryforprison","presidenttrump","makeamericagreatagain","hilary2016","trumpforpresident","alwaystrump","canadiansforbernie","cruztovictory","republicanparty","cruzcrew","2016presidentialelection","notwithher","presidentialelection2016","billclinton"]
queryList2 = ["trump","hillary2016","tedcruz","republicans","cruz2016","imwithher","hillary","democrats","conservatives","donaldtrump","voteforbernie","cruz","trump2016","makeamericahateagain","drumpf","makedonalddrumpfagain","republican","trumptrain","gop","dumptrump","clinton2016","trumprally","presidentialelection","hilaryclinton","fuckhilary","fucktrump","mrtrump","letsmakeamericagreatagain","demdebate","gopdebate","trumpisachump","aipac2016","hillaryforprison","presidenttrump","makeamericagreatagain","hilary2016","trumpforpresident","alwaystrump","canadiansforbernie","cruztovictory","republicanparty","cruzcrew","2016presidentialelection","notwithher","presidentialelection2016","billclinton"]
queryList = ["hillary2016","tedcruz","republicans","cruz2016","imwithher","hillary","democrats","conservatives","donaldtrump","voteforbernie","cruz","trump2016","makeamericahateagain","drumpf","makedonalddrumpfagain","republican","trumptrain","gop","dumptrump","clinton2016","trumprally","presidentialelection","hilaryclinton","fuckhilary","fucktrump","mrtrump","letsmakeamericagreatagain","demdebate","gopdebate","trumpisachump","aipac2016","hillaryforprison","presidenttrump","makeamericagreatagain","hilary2016","trumpforpresident","alwaystrump","canadiansforbernie","cruztovictory","republicanparty","cruzcrew","2016presidentialelection","notwithher","presidentialelection2016","billclinton"]
#queryList = ["feelthebern","wewantbernie","stillsanders","presidentbernie","weendorsebernie","berniesanders2016","voteforberniesanders","vote4bernie","berniesanders","election","politics","berniesandersforpresident","bernie2016","election2016","bernie","hillaryclinton","arizona","trump","hillary2016","tedcruz","republicans","utah","cruz2016","imwithher","boise","hillary","democrats","conservatives","saltlakecity","president","donaldtrump","independents","progressive","potus","voteforbernie","cruz","liberals","trump2016","boisestate","idaho","angrydjlife","kasich2016","gawker","thedrop","promoterscomplaining","promoterproblems","rave","ravegirls","djscomplaining","djfail","clublife","edmgirls","edmlife","makeamericahateagain","drumpf","hitler","makedonalddrumpfagain","republican","trumptrain","gop","beardedvillains","dumptrump","funny","clinton2016","cannabis","wolfblitzer","cannabiscommunity","funnyshit","trumprally","presidentialelection","voldemort","hilaryclinton","fuckhilary","doloresumbridge","fucktrump","wizard","saveus","harrypotter","hogwarts","jkrowling","newyorkcity","monday","newyork","mrtrump","fail","america","fails","lmao","usa","lol","ny","hilarious","letsmakeamericagreatagain","nyc","us","cuba","mondaymotivation","vegan","nonas","raw","lootcrate","beyondwonderland","demdebate","blacklivesmatter","vote","batmanvsuperman","thewalkingdead","obama","gameofthrones","nationalfragranceday","dccomics","gopdebate","cali","politicalrevolution","easter","phsociopoliticalissues","vscophilippines","1goodvote","eleksyon2016","kirk","kobayashimaru","captainkirk","startrek","nowallforribbert","ribbert4prez","trumpisachump","voteforme","aipac2016","ivoted","hillaryforprison","foxnews","getoutandvote","presidenttrump","makeamericagreatagain","maga","trusted","hilary2016","aipac","marchmadness","trumpforpresident","victory","cnn","alwaystrump","canadiansforbernie","cruztovictory","republicanparty","reagan","azprimary","2a","gunowners","cruzcrew","utprimary","muhroads","ojandtoothpaste","haggiswatermelon","donttreadonme","2016presidentialelection","onionandbananajuice","notwithher","pepperonidogfart","marcorubio","democratparty","presidentialelection2016","dietmountaindew","pololitics","couch","lays","libertarianparty","anarchist","bencarson","billclinton","clarkcollege","isthisit"]
#queryList = ["GOPDebate","DemDebate","election2016","usaElection2016","#debates"]
#random.shuffle(queryList)
counter = 0
for query in queryList:
    if len(searched_tweets) > max_tweets:
        break
    print query
    last_id = -1
    query_tweets = []
    while len(query_tweets) < individual_hash_level:
        count = max_tweets - len(query_tweets)
        try:
            new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1) , lang = "es")
            counter += 1
            print "counter :  " + str(counter)
            if counter % 150 == 0:
                print "Sleeping"
                time.sleep(16*60)
            if not new_tweets:
                break
            query_tweets.extend(new_tweets)
            

            print "Fetched count "+str(int(time.time())) + " : " + str(len(new_tweets))
            last_id = new_tweets[-1].id
            q_list = [query] * len(new_tweets)
            q_tags.extend(q_list)
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break
    searched_tweets.extend(query_tweets)
    print "Data size: " + str(len(query_tweets))
    #time.sleep(10)

print "Fetched: " + str(len(searched_tweets))
print len(q_tags)
fh = open("data.csv", 'w')
for tweet, q in zip(searched_tweets, q_tags):
    #print q
    fh.write(str(tweet.lang) + "," + q +","+str(tweet.retweeted) + ",'"+str(tweet.user.id) + ",'" + str(tweet.id) + "," + str(tweet.created_at) + "," +  " " + "," +  " " + "," +  " " + "," +  " " + "," +  " " + "," +  " " + "," +tweet.text.replace('\n', ' ').replace('\r', ' ').replace(',', ' ') + '\n')

#frozen = jsonpickle.encode(searched_tweets[0])
#print frozen

#translation_iter = gs.translate(t_list,'en')
#translation = list(translation_iter)
#print translation
fh.close
