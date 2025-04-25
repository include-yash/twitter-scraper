import asyncio
import csv
import os
from langdetect import detect
from main import fetch_tweets
from translate import translate_text
from sentiment import predict_sentiment, ROBERTA_SUPPORTED_LANGUAGES

# Utility function to detect language safely
def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception as e:
        print(f"⚠️ Could not detect language for: {text} -> {e}")
        return "unknown"

# Async wrapper
async def analyze():
    print("🔍 Starting tweet analysis...\n")
    tweets = await fetch_tweets()

    # Set up CSV
    with open('analyzed_tweets.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Username', 'Original Text', 'Processed Text', 'Language', 'Sentiment', 'Retweets', 'Likes', 'Created At'])

        for tweet in tweets:
            original_text = tweet['text']
            lang = detect_language(original_text)

            # Decide if translation is needed
            if lang in ROBERTA_SUPPORTED_LANGUAGES:
                processed_text = original_text
            else:
                processed_text = translate_text(original_text)
                if processed_text is None:
                    processed_text = "[Translation failed]"

            sentiment = predict_sentiment(processed_text)

            writer.writerow([
                tweet['username'],
                original_text,
                processed_text,
                lang,
                sentiment,
                tweet['retweets'],
                tweet['likes'],
                tweet['created_at']
            ])

            print(f"✅ @{tweet['username']} | {lang} | {sentiment}")

    print("\n📁 Analysis complete. Results saved to 'analyzed_tweets.csv'.")

# Run
if __name__ == '__main__':
    asyncio.run(analyze())
