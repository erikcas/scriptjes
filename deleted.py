import json
import tweepy
import sys
from tweepy import Stream
from tweepy import StreamListener
from post import post_deleted_tweet

log = open('log_deleted.log', 'a')
sys.stdout = log

print('Let the game begin')
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

class DeletedListener(StreamListener):
    
    def on_data(self, data):
            
        json_data = json.loads(data)
        
        #Filter alleen de tweets door Kaffie eruit
        try:
            if json_data['user']['id_str'] == '1347228691819077632':
                print('Voila, een tweet van onze praatzanger?')
                text_file = open(json_data['id_str']+'_Kaffie.json', 'a')
                #json.dump(data, text_file, indent=4)
                text_file.write(data)
                text_file.close()
        except KeyError:
            print('Misschien een deleted tweet?')

        try:
            if 'delete' in data:
                print(' Ah een gedelete tweet jongens')
                text_file = open(json_data['delete']['status']['id_str']+'_deleted_Kaffie.json', 'a')
                #json.dump(data, text_file, indent=4)
                text_file.write(data)
                text_file.close()
                # Post de tweet naar een wordpress
                print('Posten maar')
                tweet_id = json_data['delete']['status']['id_str']
                post_deleted_tweet(tweet_id)
        except KeyError:
            print("Och nee toch, een error. We skippen deze")
            
        return True

listener = DeletedListener()
twitterStream = Stream(auth, listener)
twitterStream.filter(follow=['1347228691819077632'])
