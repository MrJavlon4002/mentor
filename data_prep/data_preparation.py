from data_prep.tahrirchi import preprocess_text
from data_prep.text_splitter import split_text
import json
from langdetect import detect_langs
from general.openai_call import call_llm_with_functions

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

def prepare_data(text, languages=['uz', 'ru']):
    # Preprocess text
    formatted_data = preprocess_text(text)
    splitted_data = split_text(formatted_data, 2000, 10)
    
    # System prompt for titling
    def get_sys_prompt(lang):
        return f"""
        You are an AI assistant tasked with titling text. Take a provided text (less than 2000 characters) as input. 
        Treat the text as a single unit without splitting it. Generate a clear and detailed title that fully reflects 
        its content. Exclude any sentences that do not fit the text's context. Format the response as a JSON object 
        with a "title" (string) and "text" (string), following this structure: {{"title": str, "text": str}}. 
        Ensure the title is specific and descriptive, capturing the essence of the text without altering its content. 
        The title must be in the {lang} language.
        """
    
    data = {}
    for lang in languages:
        data[lang] = {}
        
        for i, chunk_text in enumerate(splitted_data):
            
            response = call_llm_with_functions(chunk_text, get_sys_prompt(lang))
            cleaned_response = response.strip().replace('```json', '').replace('```', '').replace('\n', '')
            json_data = json.loads(cleaned_response)
            
            data[lang][f"chunk_{i}"] = {
                'title': json_data['title'],
                'text': json_data['text']
            }

    return data