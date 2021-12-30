#!/usr/local/bin/python3.10

import json
import tweepy
import sys
from tweepy import Stream
from tweepy import StreamListener
#from post import post_deleted_tweet
from tweeps import tweeps
from urllib3.exceptions import ProtocolError
#from capture import tweet_screenshot
import logging

logging.basicConfig(filename='log_deleted.log', 
        filemode = 'a',
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level=logging.DEBUG)

logging.info('[SCRIPT]: Let the game begin')
# Get the twitter credentials from a (hidden) file
secrets = open(".login")
login = secrets.readlines()

# assign the values accordingly
# strip the linebreak from the values to prevent bad login errors
consumer_key = login[0].rstrip('\n')
consumer_secret = login[1].rstrip('\n')
access_token = login[2].rstrip('\n')
access_token_secret = login[3].rstrip('\n')

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth)

twitteraars = tweeps()

class UserListener(StreamListener):
    
    def on_data(self, data):
            
        json_data = json.loads(data)
        
        #Filter alleen de tweets door User eruit
        try:
            if json_data['user']['id_str'] in twitteraars:
                twitteraar = json_data['user']['id_str']
                scherm_naam = json_data['user']['screen_name']
                logging.debug(f'[SCRIPT]: Voila, een tweet van onze vriend {scherm_naam}?')
                file_prefix = f'{scherm_naam}_'
                text_id = json_data['id_str']
                text_file = open(file_prefix + json_data['id_str'] + '.json', 'w')
                text_file.write(data)
                text_file.close()
                # Maak een screenshot
                #tweet_screenshot(tweet_id, scherm_naam)
        except KeyError:
            logging.debug('[SCRIPT]: Misschien een deleted tweet?')

        try:        
            if 'delete' in data:
                logging.debug('[SCRIPT]: Ah een gedelete tweet jongens')
                twitteraar = json_data['delete']['status']['user_id']
                twitteraar = str(twitteraar)
                logging.debug(f"[SCRIPT]: {twitteraar}")
                filet = json_data['delete']['status']['id_str']+'_deleted.json'
                logging.debug(f"[SCRIPT]: filenaam {filet}")
                text_file = open(json_data['delete']['status']['id_str']+'_deleted.json', 'w')
                text_file.write(data)
                text_file.close()
                # Post de tweet naar een wordpress
                logging.debug('[SCRIPT]: Posten maar')
                tweet_id = json_data['delete']['status']['id_str']
                timestamp = json_data['delete']['timestamp_ms']
                logging.debug(f"[SCRIPT]: tweet_id: {tweet_id} || timestamp: {timestamp}")
                #post_deleted_tweet(tweet_id, timestamp)

        except KeyError as error:
            logging.debug(f"[SCRIPT]: Och nee toch, een error. We skippen deze. We zochten tweet {tweet_id}. Fout:\n{error}")
            
        return True

    def on_error(self, status):
        print(status)

listener = UserListener()
twitterStream = Stream(auth, listener)
while True:
    try:
        twitterStream.filter(follow=twitteraars)
    except (ProtocolError, AttributeError):
        continue
