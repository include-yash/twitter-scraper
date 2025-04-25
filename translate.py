from deep_translator import GoogleTranslator

def translate_text(original_text: str) -> str:
    try:
        # Translate the original text using deep-translator's GoogleTranslator
        translated_text = GoogleTranslator(source='auto', target='en').translate(original_text)
        
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

# Example text to translate
original_text = "나는 지금 그를 죽이고 싶어"  # Korean: "I want to kill him now"
translated_text = translate_text(original_text)

# print(f"Original: {original_text}")
# print(f"Translated: {translated_text}")
