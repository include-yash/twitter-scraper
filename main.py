from twikit import Client, TooManyRequests
from configparser import ConfigParser
from datetime import datetime
import time
from random import randint

async def fetch_tweets(query='gemini', minimum_tweets=10):
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    client = Client(language='en-US')

    try:
        client.load_cookies('cookies.json')
    except:
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        client.save_cookies('cookies.json')

    tweet_count = 0
    tweets = None
    results = []

    while tweet_count < minimum_tweets:
        try:
            tweets = await client.search_tweet(query, product='Top') if tweets is None else await tweets.next()
        except TooManyRequests as e:
            wait_time = e.rate_limit_reset - datetime.now().timestamp()
            time.sleep(wait_time)
            continue

        if not tweets:
            break

        for tweet in tweets:
            tweet_count += 1
            results.append({
                "username": tweet.user.name,
                "text": tweet.text,
                "created_at": tweet.created_at,
                "retweets": tweet.retweet_count,
                "likes": tweet.favorite_count
            })

            if tweet_count >= minimum_tweets:
                break

    return results
