import google.generativeai as genai
import api_keys

gemini_model = "gemini-2.0-flash"

def call_llm_with_functions(messages: str, system_instruction: str):
    """
    Call the Gemini API with tools and handle responses or errors gracefully.
    """
    genai.configure(api_key=api_keys.GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name=gemini_model,
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