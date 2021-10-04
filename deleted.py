import json
import tweepy
from tweepy import Stream
from tweepy import StreamListener

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

class CassieListener(StreamListener):
    
    def on_data(self, data):
            
        json_data = json.loads(data)
        
        #Filter alleen de tweets door Kaffie eruit
        try:
            if json_data['user']['id_str'] == '1347228691819077632':
                text_file = open(json_data['id_str']+'_Kaffie.json', 'a')
                #json.dump(data, text_file, indent=4)
                text_file.write(data)
                text_file.close()
                
            if 'delete' in data:
                print(' Ah een gedelete tweet jongens')
                text_file = open(json_data['id_str']+'_deleted_Kaffie.json', 'a')
                #json.dump(data, text_file, indent=4)
                text_file.write(data)
                text_file.close()
        except KeyError:
            print("Oh jee, een error. We skippen deze")
            
        return True

listener = CassieListener()
twitterStream = Stream(auth, listener)
twitterStream.filter(follow=['1347228691819077632'])
