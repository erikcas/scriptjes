# Twitter stream usage

Tested with python3.8

This script listens to a number of given twitter_id's. When a tweet is posted, the complete twitter metadata is saved to a json file

The filename is <username>_<tweet_id>.json

When this tweep deletes a tweet, the stream will catch it and save it to <deleted_tweet_id>_deleted.json. When enabled, the post.py script will read the original tweet (when available) and post it to a wordpress. On request, I can make it being written to a (expanding) .csv for example.

Install:

On ubuntu:

`sudo apt-get install python3 python3-pip`

`git clone https://github.com/erikcas/scriptjes.git -b stream`

`cd scriptjes`

`pip3 install -r requirements.txt`

Obtain twitter api credentials: https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api

create a file named .login and paste your credentials in below order
* api key
* api secret
* acces token
* acces secret

Optional: for posting to a wp site, enable the api in wordpress and create a .wp-login file with:
* username
* password

and put the correct url on this line in post.py:

`url = "https://<wordpress-url>/wp-json/wp/v2/posts"`

For now, wp posting is disabled but it can be easily enabled by uncommenting 2 lines:

`#from post import post_deleted_tweet`

........

........

`#post_deleted_tweet(tweet_id, timestamp)`

For catching your favorite tweeps tweets, convert his or hers (current) username to a twitter id here: https://tweeterid.com/

Put the (numeric) twitter id in a file called ".tweeps". One per line. There is a maximum rate limit (todo: how much was it again?) and fire up the script:
`python3 deleted.py`

As it is a stream, it will run forever untill you hit control+c or close the window. Suggestions:

Linux: Use screen application

On ubuntu, I installed it as a user service:

**IMPORTANT**

Change line 1 of the file deleted.py to the proper python command in your environment!

`#!<path_to_python3>`

in ubuntu find it by the output of:

`which python3`

The output will for example be:

`/usr/bin/python3`

So for this expample, line 1 of deleted.py must be:

`#!/usr/bin/python3`

Open the file stream.service and change <username> to your username

Enable lingering (else the service will not start automatically afer a reboot)

`sudo loginctl enable-linger <username>`

Copy the service file to the proper location:

`sudo cp stream.service /etc/systemd/user/`

Let the system know we added a service:

`systemctl --user daemon-reload`

Enable the service on the system, so it will start as a service on boot:

`systemctl --user enable stream`

And start it:

`systemctl --user start stream`

Check its status:

`systemctl --user status stream`

(If the output is other then "Active: active (running) since"..... please check if you can find the issue in /var/log/syslog (on ubuntu that is) else let me know)

For chromedriver: see https://skolo.online/documents/webscrapping/
