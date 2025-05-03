from data_prep.tahrirchi import preprocess_text, translate_text
from data_prep.text_splitter import split_text
import json
from langdetect import detect_langs
from general.gemini_call import call_gemini_with_functions
import time

def language_detection(query: str) -> str:
    """
    Detect language of input text and return standardized language code.
    Returns 'en' for English and similar languages,
    'ru' for Russian, and 'uz' as default.
    """
    lang_list = detect_langs(query)

    for lang in lang_list:
        lang_str = str(lang).split(':')[0]
        if lang_str in ['en', 'fi', 'nl']:
            return 'en'
        elif lang_str in ['ru', 'uk', 'mk']:
            return 'ru'
    return 'uz'

def prepare_data(text, languages = ['uz', 'ru']):
    
    source_lang = language_detection(text)

    
    formatted_data = preprocess_text(text)
    splitted_data = split_text(formatted_data, 2000, 10)

    sys_prompt = """
    You are an AI assistant tasked with titling text. Take a provided text (less than 2000 characters) as input. Treat the text as a single unit without splitting it. Generate a clear and detailed title that fully reflects its content. Exclude any sentences that do not fit the text's context. Format the response as a JSON object with a "title" (string) and "text" (string), following this structure: {"title": str, "text": str}. Ensure the title is specific and descriptive, capturing the essence of the text without altering its content. It have to be in the same language as the text.
    """

    data = {}
    for lang in languages:
        data[lang] = {}

    for i, chunk_text in enumerate(splitted_data):
        response = call_gemini_with_functions(chunk_text, sys_prompt)
        cleaned_response = response.strip().replace('```json', '').replace('```', '').replace('\n', '')
        json_data = json.loads(cleaned_response)

        title = json_data['title']
        text = json_data['text']

        data[source_lang][f"chunk_{i}"] = {
            'title': title,
            'text': text
        }

        for lang in languages:
            if lang != source_lang:
                time.sleep(1.3) 
                translated_title = translate_text(json_data['title'], source_lang, lang)
                translated_text = translate_text(json_data['text'], source_lang, lang)

                data[lang][f"chunk_{i}"] = {
                    'title': translated_title,
                    'text': translated_text
                }
                print(data[lang][f"chunk_{i}"])
    return data
