import requests
import api_keys
import re

endpoint = "https://websocket.tahrirchi.uz/translate-v2"

headers = {
    "Authorization": f"{api_keys.TAHRIRCHI_API_KEY}",
    "Content-Type": "application/json"
}


def preprocess_text(text):
    text = re.sub(r'[^\w\s\-\nа-яА-ЯёЁўЎқҚғҒҳҲ,.!?]', '', text)
    text = re.sub(r'\n\s+\n', '\n\n', text) 
    return text

def translate_text(text, source_lang, target_lang, model="tilmoch"):
    lang_map = {
        'uz': "uzn_Latn",
        'ru': 'rus_Cyrl',
        'en': 'eng_Latn'
    }
    text = preprocess_text(text)
    payload = {
        "text": text,
        "source_lang": lang_map[source_lang],
        "target_lang": lang_map[target_lang],
        "model": model
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data['translated_text']

