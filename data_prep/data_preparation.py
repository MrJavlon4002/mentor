from data_prep.text_splitter import split_text
import json
from general.gemini_call import batch_gemini_requests
from general.agent_prompts import get_sys_prompt


async def prepare_data(text, languages=['uz', 'ru']):
    splitted_data = split_text(text, 2000, 10)
    data = {}

    for lang in languages:
        sys_prompt = get_sys_prompt(lang)
        request_pairs = [(chunk_text, sys_prompt) for chunk_text in splitted_data]
        responses = await batch_gemini_requests(request_pairs)

        data[lang] = {}
        for i, response in enumerate(responses):
            if isinstance(response, dict) and "error" in response:
                data[lang][f"chunk_{i}"] = {"title": "", "text": f"ERROR: {response['error']}"}
            else:
                cleaned_response = response.strip().replace('```json', '').replace('```', '').replace('\n', '')
                json_data = json.loads(cleaned_response)
                data[lang][f"chunk_{i}"] = {
                    'title': json_data.get("title", ""),
                    'text': json_data.get("text", "")
                }
    return data
