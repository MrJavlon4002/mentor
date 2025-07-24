import asyncio
import google.generativeai as genai
import api_keys

async def call_gemini_async(messages, system_instruction):

    genai.configure(api_key=api_keys.GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=system_instruction
    )

    def _sync_call():
        return model.generate_content(
            contents=[messages],
            generation_config=genai.types.GenerationConfig(temperature=0.3),
        )

    try:
        response = await asyncio.to_thread(_sync_call)
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return {"error": "No content found in the response."}
    except Exception as e:
        return {"error": str(e)}
    
async def batch_gemini_requests(list_of_message_instruction_pairs):
    tasks = [
        call_gemini_async(messages, sys_instr)
        for messages, sys_instr in list_of_message_instruction_pairs
    ]
    results = await asyncio.gather(*tasks)
    return results


