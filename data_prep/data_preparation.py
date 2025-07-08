from data_prep.text_splitter import split_text
import json
# from langdetect import detect_langs
from general.openai_call import call_llm_with_functions

language = {
   "uz": "Uzbek Language",
   "ru": "Russian language",
   "en": "English language",
}

def prepare_data(text, languages=['uz', 'ru']):
    splitted_data = split_text(text, 2000, 10)
    
    # System prompt for titling
    def get_sys_prompt(lang):
        return f"""
        You are an AI assistant tasked with titling text. Take a provided text (less than 2000 characters) as input. 
        All text and title you wil return HAVE TO BE in the {language[lang]}. Translate even text into {language[lang]}.
        Treat the text as a single unit without splitting it. Generate a clear and detailed title that fully reflects 
        its content. Exclude any sentences that do not fit the text's context. Format the response as a JSON object 
        with a "title" (string) and "text" (string), following this structure: {{"title": str, "text": str}}. 
        Ensure the title is specific and descriptive, capturing the essence of the text without altering its content. 
        """
    
    data = {}
    for lang in languages:
        data[lang] = {}
        
        for i, chunk_text in enumerate(splitted_data):
            
            response = call_llm_with_functions(chunk_text, get_sys_prompt(lang))
            # # cleaned_response = response.strip().replace('```json', '').replace('```', '').replace('\n', '')
            # json_data = json.loads(cleaned_response)
            
            data[lang][f"chunk_{i}"] = {
                'title': "chunk_" + str(i),
                'text': chunk_text
            }

    return data