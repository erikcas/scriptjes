import json
import requests
import base64
import sys

log = open('log_post.log', 'a')
sys.stdout = log

def post_deleted_tweet(tweet_id):
    secrets = open(".wp-login")
    login = secrets.readlines()
    user = login[0].rstrip('\n')
    passwd = login[1].rstrip('\n')

    credentials = user + ':' + passwd

    url = "https://kafka.dev/wp-json/wp/v2/posts"
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}

    filename = (tweet_id + '_Kaffie.json')
    
    # Posten is waar
    posten = True
    #Open de json file met de tweet
    print(f'Open {filename} en lees de inhoud')
    try:
        with open(filename) as f:
            tweet_data = json.load(f)
    except FileNotFoundError:
        print('Deze tweet kennen we niet helaas')
        posten = False

    # Alleen posten als posten waar is
    if posten == True:
        # Gegevens om te posten
       # Tijdstip van de post
        tijdstip = tweet_data['created_at']
        # Volle naam beschreven
        naam = tweet_data['user']['name']
        # (Huidige) schermnaam
        scherm_naam = tweet_data['user']['screen_name']
        # Vorige 2 samen, staat leuk voor in de post
        gegevens = f'{naam} || schermnaam @{scherm_naam}'
        #Volledige tweet text
        if 'extended_tweet' in tweet_data:
            tweettext = tweet_data['extended_tweet']['full_text']
        elif tweet_data['retweeted_status']['truncated'] == True:
            tweettext = tweet_data['retweeted_status']['extended_tweet']['full_text']
        else:
            tweettext = tweet_data['text']
        # Te posten tekst
        tweet_text = f'Oorspronkelijk getweet op {tijdstip} (LET OP! UTC tijd)\nGetweet door {gegevens}\n\n{tweettext}'
        # Titel van de post
        titel = f'Alert! {scherm_naam} deleted tweet met id {tweet_id}'
        # Nog wat relevante gegegens voor wordpress
        status = 'publish'
        categorie = 62
        # De daadwerkelijke post
        post = {
                'title' : titel,
                'status' : status,
                'content' : tweet_text,
                'categories' : categorie,
        }

        antwoord = requests.post(url , headers=header, json=post)
        print(antwoord)
