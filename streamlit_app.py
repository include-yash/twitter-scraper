# import streamlit as st
# import requests
# import pandas as pd

# # Streamlit App UI
# def main():
#     st.set_page_config(page_title="Twitter Sentiment Analyzer", layout="wide")
#     st.title("💬 Twitter Sentiment Analyzer")
#     st.write("Analyze the sentiment of tweets in any language using Roberta + Google Translate!")

#     query = st.text_input("Enter a keyword/topic", value="gemini")
#     num_tweets = st.slider("Minimum number of tweets to analyze", 5, 100, 10)

#     if st.button("Analyze"):
#         with st.spinner("Running sentiment analysis..."):
#             # Send the request to the Flask API
#             api_url = f"http://127.0.0.1:5000/analyze_tweets?query={query}&min_tweets={num_tweets}"
#             response = requests.get(api_url)
#             analyzed = response.json()

#             st.success("Done!")

#             # Display as DataFrame
#             df = pd.DataFrame(analyzed)
#             st.dataframe(df)

#             # Optional: Download CSV
#             if st.button("Download CSV"):
#                 csv = df.to_csv(index=False).encode('utf-8')
#                 st.download_button("📥 Download results", data=csv, file_name="analyzed_tweets.csv", mime='text/csv')

# if __name__ == '__main__':
#     main()
