from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig


MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
ROBERTA_SUPPORTED_LANGUAGES = ('ar', 'en', 'fr', 'de', 'hi', 'it', 'es', 'pt')

model = AutoModelForSequenceClassification.from_pretrained(MODEL)
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)

#/ save the model locally
# SAVE_DIR = "./saved_model"
# model.save_pretrained(SAVE_DIR)
# tokenizer.save_pretrained(SAVE_DIR)



# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

def predict_sentiment(text: str) -> str:
    processed_text = preprocess(text)
    encoded_input = tokenizer(processed_text, return_tensors='pt')
    output = model(**encoded_input)
    index_of_sentiment = output.logits.argmax().item()
    sentiment = config.id2label[index_of_sentiment]
    return sentiment



# text = "its nice terrorist killed people in pehelgaun"
# print(predict_sentiment(text))