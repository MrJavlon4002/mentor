import openai
import api_keys

openai_model = "gpt-4o-mini"

def call_llm_with_functions(messages: str, system_instruction: str) -> str | dict:
    """
    Call the OpenAI Chat Completions API and return the assistant’s reply,
    mirroring the behaviour of call_llm_with_functions.
    """
    # 1. Configure the client
    openai.api_key = api_keys.OPENAI_API_KEY

    chat_messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user",   "content": messages}
    ]

    try:
        # 3. Make the request (adjust model/params as desired)
        response = openai.chat.completions.create(
            model=openai_model,
            messages=chat_messages,
            temperature=0.3
        )

        # 4. Extract and return the assistant text
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return {"error": "No content found in the response."}

    except Exception as e:
        print(f"Error during OpenAI call: {e}")
        return {"error": str(e)}
