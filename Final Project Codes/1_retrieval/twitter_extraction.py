import tweepy
import random
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sys
import jsonpickle
reload(sys)
sys.setdefaultencoding("utf-8")


consumer_key = []
consumer_secret = []
access_token = []
access_secret = []



# Adding all the consumer keys
consumer_key.extend(['kZyMSZBRORZaDdutIIMja6v85'])
consumer_secret.extend(['Mbu2HqI0Ea6MSIRr3B7MKgMSxEdQpJXqOEb4n4oAMLLulQxDXm'])
access_token.extend(['84823887-ZAiJrvVV5WxmSiTnOUdya2ZzNjur7DCL4Xkyoia5r'])
access_secret.extend(['3Hf0OAKKtue0TPOcFkCcgK153eOKv4dCoqcQOAC1rzIMy'])

access_token.extend(["74693581-fOWOuGkCBKYyYWdHiCCIvmxB6V3aSry7LxhSojWiA"])
access_secret.extend(["3YppAZgpqjGGhHg9XpQPaneKqYOvUiT6tz1ZAjwry5LNw"])
consumer_key.extend(["HQNUFeGBA3vCuebSS2T51a7Wt"])
consumer_secret.extend(["3NhJIU6J4aHpYbJlOyQ75Yjko4JGHBD4fgmwjAn1tlQ7duiPpe"])

consumer_key.extend(["BlweSNHSKmeSur5YkXMxzkUUV"])
consumer_secret.extend(["KocCMLcrY4u34eqt2UNSm9wk89MZdrRSjKfZdzJxVgKNT56aCI"])
access_token.extend(["4317032720-yxQUoRRj6SZtDSSf7RsgvSCjukEHFNbQGbWJPpY"])
access_secret.extend(["UWRd46OzsWezffVASlQpzgJ8EMUcX2HHZPFadw4bM7K9k"])

consumer_key.extend(['BuamdDtGgiUMFjPX0j1ZGfFuU'])
consumer_secret.extend(['r06YXs2wRePrsCMOdWWMxKBDUP7AEjZLmzcuxSNYHvuQB8ynXc'])
access_token.extend(['108324710-FNh5JrXEMMycUqKum5GSCKDjzYSGN0qhypGN1S4v'])
access_secret.extend(['JIpQZ7z23NiQqtkFSR8GEEvaPPUlF44w9zB0tkvkU5JFY'])
	

#Rotate the authentication keys in case of key exhaustion
def rotateSecurity(index):
	mod = 4	
	print "index : "+str(index)
	if index == -1:
		index = 0
	else:
		index = (index+1)%mod
		if index == 0:
			print "Sleeping"
			time.sleep(16*60)

	auth = tweepy.auth.OAuthHandler(consumer_key[index], consumer_secret[index])
	auth.set_access_token(access_token[index], access_secret[index])
	api = tweepy.API(auth)
	return [auth , api , index]

#Initialize with the first security code
auth , api , key = rotateSecurity(-1)


searched_tweets = []
last_id = -1

#Upper Limit of corpus size
max_tweets = 3000000
individual_hash_level = max_tweets
q_tags = []

#Hashtags identified for the primary elections
queryList = ["feelthebern","wewantbernie","stillsanders","presidentbernie","weendorsebernie","berniesanders2016","voteforberniesanders","vote4bernie","berniesanders","berniesandersforpresident","bernie2016","election2016","bernie","hillaryclinton","trump","hillary2016","tedcruz","republicans","cruz2016","imwithher","hillary","democrats","conservatives","donaldtrump","voteforbernie","cruz","trump2016","makeamericahateagain","drumpf","makedonalddrumpfagain","republican","trumptrain","gop","dumptrump","clinton2016","trumprally","presidentialelection","hilaryclinton","fuckhilary","fucktrump","mrtrump","letsmakeamericagreatagain","demdebate","gopdebate","trumpisachump","aipac2016","hillaryforprison","presidenttrump","makeamericagreatagain","hilary2016","trumpforpresident","alwaystrump","canadiansforbernie","cruztovictory","republicanparty","cruzcrew","2016presidentialelection","notwithher","presidentialelection2016","billclinton","whichhillary","releasethetranscripts"]
print len(queryList)
fw = open("corpus.csv", 'w')
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
            query1 = "#"+query
            #Calling twitter to extract tweets
            new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1) , lang = "es")
            counter += 1
            print "counter :  " + str(counter)
            #checking limit of the key
            if counter % 150 == 0:
            	auth , api , key = rotateSecurity(key)
            if not new_tweets:
                break
            query_tweets.extend(new_tweets)
            for tweet in new_tweets:
                #writing into the corpus after each request
                fw.write(str(tweet.lang) + "," + query +","+str(tweet.retweeted) + ",'"+str(tweet.user.id) + ",'" + str(tweet.id) + "," + str(tweet.created_at) + "," +  " " + "," +  " " + "," +  " " + "," +  " " + "," +  " " + "," +  " " + "," +tweet.text.replace('\n', ' ').replace('\r', ' ').replace(',', ' ') + '\n')
            print "Fetched count "+str(int(time.time())) + " : " + str(len(new_tweets))
            last_id = new_tweets[-1].id
            q_list = [query] * len(new_tweets)
            q_tags.extend(q_list)
        except tweepy.TweepError as e:
            break
    searched_tweets.extend(query_tweets)
    print "Data size: " + str(len(query_tweets))

print "Fetched: " + str(len(searched_tweets))
print len(q_tags)
fw.close()
