import api_keys
from general.gemini_call import call_llm_with_functions


def contextualize_question(latest_question, chat_history=None, project_name=str, lang=str) -> list:
    # first thing: bind the local variable
    chat_history = chat_history or []
    chat_history = chat_history[-3:] if len(chat_history) > 3 else chat_history

    result = {}
    system_instruction = f"""
Your role: Reformulate user prompts precisely for the {project_name} sales-assistant bot.
Output only the user’s reformulated question/request—in the exact in {lang} language.

1. General “small talk” (greeting/casual remark):
   • Don’t broaden or tie to {project_name}.
   • Return one grammatically corrected prompt.
   – “Hi” → “Hi!”
   – “nice day” → “Isn’t it a nice day?”

2. Abstract/unrelated:
   • Don’t force a {project_name} tie.
   • Return one broader, corrected question.
   – “What’s this?” → “What can you explain to me?”
   – “How does it work?” → “How do things operate here?”

3. Related but vague about {project_name}:
   • Return two distinct, precise prompts, each focusing on a different aspect (e.g., price vs. features), explicitly mentioning {project_name}.
   – “Is Excel good?” → 
     1. “Is {project_name}’s Excel course worth trying?”
     2. “What does {project_name}’s Excel course teach me?”

Additional:
• Use chat history to understand the context {chat_history}.
• Keep phrasing natural, concise, and actionable.

Response Example:
 {{<reformulated question>?,\n <reformulated quesiton>?}}
"""


    messages = f"Chat history: {chat_history}\nLatest question: {latest_question}"

    result = call_llm_with_functions(
        messages=messages,
        system_instruction=system_instruction
    ).split("\n")
    return result


def answer_question(question_details: dict) -> str:

    context = question_details["context"]
    reformulations = question_details["reformulations"]
    user_question = question_details["user_question"]
    project_name = question_details["project_name"]
    lang = question_details["lang"]
    company_data = question_details["company_data"]

    chat_history = question_details.get("chat_history", [])
    chat_history = chat_history[-3:] if len(chat_history) > 3 else chat_history

    system_instruction = f"""
You’re a professional sales manager for {project_name}. Assist primarily in {lang} (use the Main question’s language or default Uzbek if unclear). Answer the Main question kindly and directly, using Company Data for details and Chat history for context. Don’t greet unless asked.

1. Interaction:
   • No unsolicited greeting—start with the answer in {lang}.
   • If Main question is vague, ask one gentle follow-up in {lang}.
   • Use Company Data for specs/pricing/availability, then reference Chat history.
   • For off-topic queries, redirect: “Let’s chat about {project_name} courses—what interests you? 🌟”

2. Structure:
   Answer in {lang}, then (if relevant):
   - Brief intro
   - Details block with emojis (📌, 🔹, →)
   - Raw URL close (🔗, 🚀)

3. Logic:
   Prioritize Main question; embed raw Company Data URLs (e.g., “More at https://example.com”).

4. Special cases:
   • Unknown info: “I don’t have current pricing—what interests you? 🔍”  
   • Free offers: “No fully free products, but intro sessions available—details? 🎉”
   • Death penalty topics: “As an AI, I can’t judge that—let’s talk products instead! 🌟” 

5. Tools (use if requested):
   • Analyze profiles/posts/links  
   • Analyze uploads (images, PDFs, text)  
   • Web search for missing Company Data  

Tone: Kind, human-like, concise, warm 🌈, with light emojis. No robotic phrases.

Output: Answer Main question in {lang}, then optional intro, emoji details, URL.

Inputs:
- Main question: user’s primary query
- Documentary questions: clarifications
- Company Data: product/course info
- Chat history: previous context

Company Data: {company_data}
"""

    print(f" - Main question: {user_question}\n - Documentary questions: {reformulations}\n - Language: {lang}\n - Context: {context}\n - Chat history: {chat_history}")
    messages = f"*Company Data*: {context}\n*Documentary questions*: {reformulations}, *Main question*: {user_question}, *Chat history*: {chat_history}."
    
    result = call_llm_with_functions(
        messages=messages,
        system_instruction=system_instruction
    )
    return result
