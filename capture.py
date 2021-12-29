from tweetcapture import TweetCapture
import asyncio
import logging
from selenium.common.exceptions import WebDriverException

logging.basicConfig(filename='log_deleted.log',
        filemode = 'a',
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level=logging.DEBUG)

tweet = TweetCapture()

def tweet_screenshot(tweet_id, scherm_naam):
    url = f'https://twitter.com/{scherm_naam}/status/{tweet_id}'
    print(url)
    output = f'screenshots/{scherm_naam}_{tweet_id}.png'
    try:
        asyncio.run(tweet.screenshot(url, output, mode=2, night_mode=0))
    except WebDriverException as e:
        logging.debug(f'no screenshot made. Error {e}')
