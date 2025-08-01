from general.gemini_call import call_gemini_async
import general.agent_prompts as prompts
import json


async def contextualize_question(latest_question, chat_history, project_name=str, agent_type=str, lang=str) -> list:
    # first thing: bind the local variable
   chat_history = chat_history or []
   chat_history = chat_history[-3:] if len(chat_history) > 3 else chat_history


   system_instruction = prompts.reformulation_prompt(agent_type=agent_type, project_name=project_name, lang=lang,)
   messages = f"CHAT HISTORY: {chat_history}\nLatest question: {latest_question}"


   result = (await call_gemini_async(
       messages=messages,
       system_instruction=system_instruction
   )).split("\n")


   return result


async def answer_question(question_details: dict) -> str:
   chat_history = question_details["history"] or []
   agent_prompts = {
      "sales": prompts.sales_agent_prompt,
      "support": prompts.customer_support_agent_prompt,
      "staff": prompts.staff_training_agent_prompt,
      "q/a": prompts.question_answer_agent_prompt
   }

   prompt_function = agent_prompts[question_details["service_type"]]
   if prompt_function:
      system_instruction = prompt_function(
         project_name=question_details["project_name"],
         company_data=question_details["company_data"],
         lang=question_details["lang"]
      )


   # print(f" - Main question: {question_details['user_question']}\n - Documentary questions: {question_details['reformulations']}\n - Language: {question_details['lang']}\n - Context: {question_details['context']} \n - Chat history: {chat_history}")
   
   

   messages = f'*Company Data*: {question_details["context"]}\n*Documentary questions*: {question_details["reformulations"]}, *Main question*: {question_details["user_question"]}, *Chat history*: {chat_history}.'

   response = await call_gemini_async(
       messages=messages,
       system_instruction=system_instruction
   )

   cleaned_response = response.strip().replace('```json', '').replace('```', '').replace('\n', '')
   json_data = json.loads(cleaned_response)

   return json_data
