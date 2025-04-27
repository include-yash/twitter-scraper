from twikit import Client, TooManyRequests, Unauthorized
from datetime import datetime
import streamlit as st
import time

async def fetch_tweets(query='gemini', minimum_tweets=10):
    # Load credentials from Streamlit secrets
    username = st.secrets["credentials"]["username"]
    email = st.secrets["credentials"]["email"]
    password = st.secrets["credentials"]["password"]

    client = Client(language='en-US')

    try:
        # Load cookies if available
        client.load_cookies('cookies.json')

        # Check if cookies are valid: harmless call instead of `client.me()`
        try:
            await client.get_tweet_detail(tweet_id="20")  # Random public tweet id
        except Unauthorized:
            await client.login(auth_info_1=username, auth_info_2=email, password=password)
            client.save_cookies('cookies.json')
    except Exception:
        # If cookies don't exist or loading fails, login
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
            st.warning(f"Rate limit hit. Waiting {int(wait_time)} seconds...")
            time.sleep(wait_time)
            continue
        except Unauthorized:
            await client.login(auth_info_1=username, auth_info_2=email, password=password)
            client.save_cookies('cookies.json')
            continue

        if not tweets:
            st.warning("No more tweets found.")
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
