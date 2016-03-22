import tweepy
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
consumer_key = 'BuamdDtGgiUMFjPX0j1ZGfFuU'
consumer_secret = 'r06YXs2wRePrsCMOdWWMxKBDUP7AEjZLmzcuxSNYHvuQB8ynXc'
access_token = '108324710-FNh5JrXEMMycUqKum5GSCKDjzYSGN0qhypGN1S4v'
access_secret = 'JIpQZ7z23NiQqtkFSR8GEEvaPPUlF44w9zB0tkvkU5JFY'


auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


proxy_handler = urllib2.ProxyHandler({"http" : "http://52.10.153.135:8083"})
proxy_opener = urllib2.build_opener(urllib2.HTTPHandler(proxy_handler),
                                    urllib2.HTTPSHandler(proxy_handler))

#gs = goslate.Goslate(opener=proxy_opener)
gs = goslate.Goslate()

fh = open("data.csv", 'w')

t_list = [] 

searched_tweets = []
last_id = -1
max_tweets = 3000
query = "gopDebate"
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        print "Fetched: " + str(len(new_tweets))
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

print "Fetched: " + str(len(searched_tweets))

for tweet in searched_tweets:
	fh.write(str(tweet.lang) + "," + str(tweet.retweeted) + "," + str(tweet.created_at) + "," + tweet.text[2:].replace('\n', ' ').replace('\r', ' ') + '\n')

#frozen = jsonpickle.encode(searched_tweets[0])
#print frozen

#translation_iter = gs.translate(t_list,'en')
#translation = list(translation_iter)
#print translation
fh.close
