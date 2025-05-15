from general.gemini_call import call_llm_with_functions
import general.agent_prompts as prompts


def contextualize_question(latest_question, chat_history, project_name=str, agent_type = str, lang=str) -> list:
    # first thing: bind the local variable
   chat_history = chat_history or []
   chat_history = chat_history[-3:] if len(chat_history) > 3 else chat_history


   system_instruction = prompts.reformulation_prompt(agent_type=agent_type, project_name=project_name, lang=lang,)
   messages = f"CHAT HISTORY: {chat_history}\nLatest question: {latest_question}"


   result = call_llm_with_functions(
       messages=messages,
       system_instruction=system_instruction
   ).split("\n")

   return result


def answer_question(question_details: dict) -> str:
   chat_history = question_details["history"] or []
   chat_history = chat_history[-10:] if len(chat_history) > 10 else chat_history
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


   print(f" - Main question: {question_details['user_question']}\n - Documentary questions: {question_details['reformulations']}\n - Language: {question_details['lang']}\n - Context: {question_details['context']} \n - Chat history: {chat_history}")
   
   

   messages = f'*Company Data*: {question_details["context"]}\n*Documentary questions*: {question_details["reformulations"]}, *Main question*: {question_details["user_question"]}, *Chat history*: {chat_history}.'
   
   result = call_llm_with_functions(
       messages=messages,
       system_instruction=system_instruction
   )

   return result