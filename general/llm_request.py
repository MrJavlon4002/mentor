from general.gemini_call import call_llm_with_functions
import general.agent_prompts as prompts


def contextualize_question(latest_question, chat_history=None, project_name=str, agent_type = str, lang=str) -> list:
    # first thing: bind the local variable
    chat_history = chat_history or []
    chat_history = chat_history[-3:] if len(chat_history) > 3 else chat_history

    result = {}
    system_instruction = prompts.reformulation_prompt(agent_type=agent_type, project_name=project_name, lang=lang,)


    messages = f"CHAT HISTORY: {chat_history}\nLatest question: {latest_question}"

    result = call_llm_with_functions(
        messages=messages,
        system_instruction=system_instruction
    ).split("\n")
    return result


def answer_question(question_details: dict) -> str:

   question_details["chat_history"] = question_details["chat_history"][-3:] if len(question_details["chat_history"]) > 3 else question_details["chat_history"]

   if question_details["service_type"] == "sales":
      system_instruction = prompts.sales_agent_prompt(project_name=question_details["project_name"], company_data=question_details["company_data"], lang=question_details["lang"])
   elif question_details["service_type"] == "support":
      system_instruction = prompts.customer_support_agent_prompt(project_name=question_details["project_name"], company_data=question_details["company_data"], lang=question_details["lang"])
   elif question_details["service_type"] == "staff":
      system_instruction = prompts.staff_training_agent_prompt(project_name=question_details["project_name"], company_data=question_details["company_data"], lang=question_details["lang"])
   elif question_details["service_type"] == "q/a":
      system_instruction = prompts.sales_agent_prompt(project_name=question_details["project_name"], company_data=question_details["company_data"], lang=question_details["lang"])


   print(f" - Main question: {question_details["user_question"]}\n - Documentary questions: {question_details["reformulations"]}\n - Language: {question_details["lang"]}\n - Context: {question_details["context"]}\n - Chat history: {question_details["chat_history"]}")
   
   

   messages = f"*Company Data*: {question_details["context"]}\n*Documentary questions*: {question_details["reformulations"]}, *Main question*: {question_details["user_question"]}, *Chat history*: {question_details["chat_history"]}."
   
   result = call_llm_with_functions(
       messages=messages,
       system_instruction=system_instruction
   )

   return result