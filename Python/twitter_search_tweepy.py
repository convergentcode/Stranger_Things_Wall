'''
This file uses the tweepy library to stream all public tweets with a hashtag chosen by the user and sends
each character to a port

To run this code you need a 'cred.yml' file in a sibling directory named 'conf'
This yml file needs four entries:
consumer_key
consumer_secret
access_token
access_token-secret

yaml format is super easy. Learn about it here: http://www.yaml.org/

'''

import tweepy
import yaml
import re
import serial
from time import sleep

conf = yaml.load(open('conf/cred.yml'))
myPort = serial.Serial('/dev/ttyUSB0', 115200, timeout = 10)

hashtag = input("Input a hashtag to search for: ")
if hashtag[0] !='#':
    hashtag='#'+hashtag
regex = re.compile('[^a-zA-Z]')
sft = re.compile(hashtag)
    
#override the tweepy stream listener class 
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            #when you retrieve a status, print it out
            print(status.author.screen_name+": " )
            print(status.text)
            print("TIMESTAMP: "+str(status.created_at)) 
            no_hashtag = sft.sub('',  status.text)
            text_only = regex.sub('', no_hashtag).encode('ascii', 'ignore')
            for character in text_only:
                print(character)
                myPort.write(character)
                sleep(0.5)
        except Exception as e:
            print(e)
            pass

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

def main():
    #authorize the connection to twitter
    auth=tweepy.OAuthHandler(conf['consumer_key'], conf['consumer_secret'])
    auth.set_access_token(conf['access_token'], conf['access_token_secret'])

    api = tweepy.API(auth)

    #while(True):
    try:
        #stream tweets indefinitely
        myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
        myStream.filter(track=[hashtag])
    except UnicodeEncodeError as e:
        print("\n")
        print(e)
        print("\n")
   

main()
