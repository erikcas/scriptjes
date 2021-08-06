from datetime import datetime
import tweepy

# Get the twitter credentials from a (hidden) file
secrets = open(".login")
login = secrets.readlines()

# assign the values accordingly
# strip the linebreak from the values to prevent bad login errors
consumer_key = login[0].rstrip('\n')
consumer_secret = login[1].rstrip('\n')
access_token = login[2].rstrip('\n')
access_token_secret = login[3].rstrip('\n')

def gevaccineerd(toen, nu = datetime.now(), interval = "default"):

    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]

    duration = nu - toen # For build-in functions
    duration_in_s = duration.total_seconds() 
    
    def jaren():
      return divmod(duration_in_s, 31536000) # Seconds in a year=31536000.

    def dagen(seconden = None):
      return divmod(seconden if seconden != None else duration_in_s, 86400) # Seconds in a day = 86400

    def uren(seconden = None):
      return divmod(seconden if seconden != None else duration_in_s, 3600) # Seconds in an hour = 3600

    def minuten(seconden = None):
      return divmod(seconden if seconden != None else duration_in_s, 60) # Seconds in a minute = 60

    def seconden(seconden = None):
      if seconden != None:
        return divmod(seconden, 1)   
      return duration_in_s

    def totalDuration():
        y = jaren()
        d = dagen(y[1]) # Use remainder to calculate next variable
        h = uren(d[1])
        m = minuten(h[1])
        s = seconden(m[1])

        return "Jeetje. 12 over 6 alweer!\nIk ben nu {} dagen, {} uren, {} minuten and {} seconden volledig gevaccineerd.\n\n".format(int(d[0]), int(h[0]), int(m[0]), int(s[0]))

    return {
        'jaren': int(jaren()[0]),
        'dagen': int(dagen()[0]),
        'uren': int(uren()[0]),
        'minuten': int(minuten()[0]),
        'seconden': int(seconden()),
        'default': totalDuration()
    }[interval]

# Example usage
toen = datetime(2021, 7, 4, 15, 5)
nu = datetime.now()

vaxxi = gevaccineerd(toen)
mijn_status = "Still: Alive and kicking! Nog steeds niet dood neergevallen. Have a nice day!"

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth)

twiet = (vaxxi + mijn_status)
api.update_status(twiet)
#print(twiet)
#TODO Als we een jaar voorbij gaan, dan even jaar toevoegen
