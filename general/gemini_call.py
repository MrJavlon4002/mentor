import google.generativeai as genai
import api_keys
from langdetect import detect_langs



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


def call_gemini_with_functions(messages: str, system_instruction: str)->list[str]:
    """
    Call the Gemini API with tools and handle responses or errors gracefully.
    """
    genai.configure(api_key=api_keys.GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system_instruction
    )

    try:
        response = model.generate_content(
            contents=[messages],
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
            ),
        )
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return {"error": "No content found in the response."}
    
    except Exception as e:
        print(f"Error during Gemini call: {e}")
        return {"error": str(e)}