import streamlit as st
import asyncio
from langdetect import detect
from main import fetch_tweets
from sentiment import predict_sentiment, ROBERTA_SUPPORTED_LANGUAGES
from translate import translate_text

# Language detector
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# Sentiment pipeline
async def run_pipeline(query, min_tweets):
    st.info("Fetching tweets...")
    tweets = await fetch_tweets(query=query, minimum_tweets=min_tweets)

    analyzed_data = []

    for tweet in tweets:
        original = tweet['text']
        lang = detect_language(original)
        if lang in ROBERTA_SUPPORTED_LANGUAGES:
            processed = original
        else:
            processed = translate_text(original) or "[Translation failed]"

        sentiment = predict_sentiment(processed)

        analyzed_data.append({
            "User": tweet['username'],
            "Original": original,
            "Processed": processed,
            "Language": lang,
            "Sentiment": sentiment,
            "Likes": tweet['likes'],
            "Retweets": tweet['retweets'],
            "Time": tweet['created_at']
        })

    return analyzed_data

# Streamlit App UI
def main():
    st.set_page_config(page_title="Twitter Sentiment Analyzer", layout="wide")
    st.title("💬 Twitter Sentiment Analyzer")
    st.write("Analyze the sentiment of tweets in any language using Roberta + Google Translate!")

    query = st.text_input("Enter a keyword/topic", value="gemini")
    num_tweets = st.slider("Minimum number of tweets to analyze", 5, 100, 10)

    if st.button("Analyze"):
        with st.spinner("Running sentiment analysis..."):
            analyzed = asyncio.run(run_pipeline(query, num_tweets))
            st.success("Done!")

            # Display as DataFrame
            st.dataframe(analyzed)

            # Optional: Download CSV
            if st.button("Download CSV"):
                import pandas as pd
                df = pd.DataFrame(analyzed)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download results", data=csv, file_name="analyzed_tweets.csv", mime='text/csv')

if __name__ == '__main__':
    main()
