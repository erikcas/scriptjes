from tweetcapture import TweetCapture
import asyncio
import logging
from selenium.common.exceptions import WebDriverException
import time
import os
logging.basicConfig(filename='log_deleted.log',
        filemode = 'a',
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level=logging.DEBUG)

tweet = TweetCapture()

cp = '<path-to-chromedriver>'
chromium = '<path/to/chromium-browser>'
def tweet_screenshot(tweet_id, scherm_naam):
    url = f'https://twitter.com/{scherm_naam}/status/{tweet_id}'
    print(url)
    output = f'screenshots/{scherm_naam}_{tweet_id}.png'
    try:
        tweet.set_chromedriver_path(cp)
        tweet.set_wait_time(7)
        asyncio.run(tweet.screenshot(url, output, mode=2, night_mode=0))
    except WebDriverException as e:
        logging.debug(f'no screenshot made. Error {e}')
        #print(f'oeps {e}')
    # Sleep 5 seconds and kill chromedriver and chrome
    logging.debug('[SCREENSHOT]Sleep 5 seconds and kill chromedriver and chrome')
    time.sleep(5)
    os.system('/usr/bin/killall <path-to-chromedriver> && /usr/bin/killall chromium)
