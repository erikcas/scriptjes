import json
import requests
import base64
import sys
import time
import logging
from fnmatch import fnmatch
from os import listdir
from read_it import convert_readable

logging.basicConfig(filename='log_deleted.log',
        filemode = 'a',
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level=logging.DEBUG)

def post_deleted_tweet(tweet_id, timestamp):
    secrets = open(".wp-login")
    login = secrets.readlines()
    user = login[0].rstrip('\n')
    passwd = login[1].rstrip('\n')

    credentials = user + ':' + passwd

    url = "https://<wordpress-url>/wp-json/wp/v2/posts"
    media_url = "https://<wordpress-url>/wp-json/wp/v2/media"
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}

    filename = 'tbd'
    tmpfile = '*' + str(tweet_id) +'.json'
    for file in listdir("."):
        if fnmatch(file, tmpfile):
            filename = file

    png_name = 'tbd'
    tmp_png = '*' + str(tweet_id) +'.png'
    for file in listdir("./screenshots"):
        if fnmatch(file, tmp_png):
            png_name = f'screenshots/{file}'

    # Posten is waar
    posten = True
    timestamp = int(timestamp) / 1000
    datetime = time.strftime('%d-%m-%Y om %H:%M:%S', time.localtime(timestamp))
    #Open de json file met de tweet
    logging.debug(f'[SCRIPT]: Open {filename} en lees de inhoud')
    try:
        with open(filename) as f:
            tweet_data = json.load(f)
    except FileNotFoundError:
        logging.debug('[SCRIPT]: Deze tweet kennen we niet helaas')
        posten = False

    logging.debug(f'[SCRIPT]: Open {png_name} en upload naar WP')
    try:
        post = {'file': open(png_name,'rb'), 'caption': png_name }
        image = requests.request(
                "POST",
                media_url,
                headers=header,
                files=post)
        resultaat = image.json()
        guid = resultaat.get('guid')
        image_url_raw = guid.get('raw')
        image_url = f'<img src={image_url_raw}>'
    except FileNotFoundError:
        logging.debug('[SCRIPT]: Geen screenshot gevonden')
        image_url = '==>SCREENSHOT NOT AVAILABLE<=='

    # Alleen posten als posten waar is
    if posten == True:
        # Gegevens om te posten
        # Tijdstip van de post
        tijdstip = tweet_data['timestamp_ms']
        tijdstip = int(tijdstip) / 1000
        tijdstip = time.strftime('%d-%m-%Y om %H:%M:%S', time.localtime(tijdstip))
        # Volle naam beschreven
        naam = tweet_data['user']['name']
        # (Huidige) schermnaam
        scherm_naam = tweet_data['user']['screen_name']
        # Avatar
        avatar = tweet_data['user']['profile_image_url']
        # Vorige 2 samen, staat leuk voor in de post
        gegevens = f'{naam} @{scherm_naam}'
        #Volledige tweet text
        tweettext = 'initieel'
        try:
            tweettext = tweet_data['extended_tweet']['full_text']
        except KeyError:
            logging.debug('[SCRIPT]: Oeps')
        try:
            tweettext = tweet_data['retweeted_status']['extended_tweet']['full_text']
        except KeyError:
            logging.debug('[SCRIPT]: Oeps')
        try:
            tweettext = tweet_data['user']['retweeted_status']['extended_tweet']['full_text']
        except KeyError:
            logging.debug('[SCRIPT]: Oeps')
        if tweettext == 'initieel':
            tweettext = tweet_data['text']
        # Even de metadata ophalen
        convert_readable(filename)
        with open('temp.json') as f:
            jsontext = f.read()
        # Te posten tekst
        #tweet_text = f'Oorspronkelijk getweet op {tijdstip} (LET OP! UTC tijd)\nGetweet door {gegevens}\n\n{tweettext}'
        tweet_text = f'<p>Onderstaande tweet op {datetime} door @{scherm_naam} verwijderd:\n\n<img src={avatar}><strong>{gegevens}</strong>\n{image_url}\n \
                {tweettext}\n <span style="font-size: 8pt;">Oorspronkelijk gepost op {tijdstip}.</span>\n \
                <!--more Klik hier voor metadata--></p><p>\n\nMetadata:\n<code><pre>{jsontext}</pre></code></p>'
        # Titel van de post
        titel = f'Alert! {scherm_naam} deleted tweet met id {tweet_id}'
        # Nog wat relevante gegegens voor wordpress
        status = 'publish'
        categorie = 2
        # De daadwerkelijke post
        post = {
                'title' : titel,
                'status' : status,
                'content' : tweet_text,
                'categories' : categorie,
        }

        antwoord = requests.post(url , headers=header, json=post)
