import time
import json
import logging
from typing import Dict, List, Any, Optional, Union

from database.vector_database import WeaviateDatabase
from general.openai_call import call_llm_with_functions
from general.llm_request import contextualize_question, answer_question
from data_prep.data_preparation import prepare_data

class DocumentHandler:
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.client = WeaviateDatabase()
        self.logger = logger or self._create_default_logger()

    def _create_default_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger

    def data_upload(self, project_id: str, row_data: str, languages: List[str]) -> None:
        try:
            processed_data = prepare_data(row_data, languages)
            self.client.initialize_and_insert_data(processed_data, project_id=project_id)
            self.logger.info(f"Data inserted for project {project_id}")
        except Exception as e:
            self.logger.error(f"Upload failed: {e}")
            raise

    def create_product(self, details: Dict[str, Any], project_id: str, lang: str) -> Dict[str, Any]:
        """
        Translates product 'name' and all fields in 'details' from source lang to each target lang.
        Preserves 'id' and 'languages'.
        """
        if 'details' not in details or 'languages' not in details:
            raise ValueError("Missing 'details' or 'languages' in product details")

        translated_data = {lang: details.copy()}
        base_lang = lang

        sys_prompt = """
    You are a professional translator.
    Translate the following product information from {source_lang} to {target_lang}.

    Product JSON:
    {product_json}

    Only translate values. Preserve all keys and structure.
    Return only valid JSON with translated values.
    """

        for target_lang in details['languages']:
            if target_lang == base_lang:
                continue

            try:
                translatable_payload = {
                    "name": details["name"],
                    "details": details["details"]
                }

                prompt = sys_prompt.format(
                    source_lang=base_lang,
                    target_lang=target_lang,
                    product_json=json.dumps(translatable_payload, ensure_ascii=False, indent=2)
                )

                response = call_llm_with_functions(
                    messages=f"{details}",
                    system_instruction=prompt
                )

                parsed = json.loads(response)
                translated = {
                    "name": parsed["name"],
                    "details": parsed["details"],
                    "id": details["id"],
                    "languages": details["languages"],
                }

                translated_data[target_lang] = translated
                self.logger.info(f"Product created for {target_lang}")


            except Exception as e:
                self.logger.error(f"Translation failed for {target_lang}: {e}")
            
            for lang in translated_data.keys():
                self.client.add_product(f"{project_id}_{lang}", translated_data[lang])

        return translated_data



    def get_product(self, project_id: str, product_id: str, languages: List[str]) -> Union[Dict[str, Any], str]:
        products = {}
        for lang in languages:
            try:
                product = self.client.get_product(project_id= f"{project_id}_{lang}", product_id= product_id)
                if product:
                    products[lang] = product
            except Exception as e:
                self.logger.warning(f"Error getting product in {lang}: {e}")

        return products if products else "Product not found"

    def update_product(self, project_id: str, details: Dict[str, Any], lang: str) -> None:
        """
        Updates a product in all specified languages.
        Translates 'name' and 'details' values. Preserves 'id' and 'languages'.
        """
        if 'languages' not in details or not details['languages']:
            raise ValueError("No 'languages' specified")
    
        base_lang = lang
    
        sys_prompt = """
        You are a professional translator.
        Translate the following product information from {source_lang} to {target_lang}.
    
        Product JSON:
        {product_json}
    
        Only translate values. Preserve all keys and structure.
        Return only valid JSON with translated values.
        """
    
        # Start with the original data
        translated_data = {base_lang: details.copy()}
    
        for target_lang in details['languages']:
            if target_lang == base_lang:
                continue
            
            try:
                translatable_payload = {
                    "name": details["name"],
                    "details": details["details"]
                }
    
                prompt = sys_prompt.format(
                    source_lang=base_lang,
                    target_lang=target_lang,
                    product_json=json.dumps(translatable_payload, ensure_ascii=False, indent=2)
                )
    
                response = call_llm_with_functions(
                    messages=f"{details}",
                    system_instruction=prompt
                )
    
                parsed = json.loads(response)
    
                translated = {
                    "name": parsed["name"],
                    "details": parsed["details"],
                    "id": details["id"],
                    "languages": details["languages"],
                }
    
                translated_data[target_lang] = translated
                self.logger.info(f"Prepared updated product for {target_lang}")
    
            except Exception as e:
                self.logger.error(f"Translation failed for {target_lang}: {e}")
    
        # Finally update all products in DB
        for lang_code, translated in translated_data.items():
            try:
                self.client.update_product(project_id=f"{project_id}_{lang_code}", details=translated)
                self.logger.info(f"Product updated for {lang_code}")
            except Exception as e:
                self.logger.error(f"Update failed for {lang_code}: {e}")



    def delete_product(self, project_id: str, product_id: str, languages: List[str]) -> bool:
        success = True
        for lang in languages:
            try:
                self.client.delete_product(f"{project_id}_{lang}", product_id)
            except Exception as e:
                self.logger.error(f"Delete failed for {lang}: {e}")
                success = False
        return success

    def query_core_data(self, project_id: str, query: str, lang: str) -> Union[List[Dict[str, Any]], str]:
        try:
            results = self.client.hybrid_query(query=query, collection_name=f"{project_id}_{lang}")
            return results if results else "No relevant data found."
        except Exception as e:
            self.logger.error(f"Query error: {e}")
            return "Query failed"

    def delete_project(self, project_id: str, languages: List[str]) -> bool:
        success = True
        for lang in languages:
            try:
                self.client.delete_collection(project_id=project_id, language=lang)
            except Exception as e:
                self.logger.error(f"Project delete failed for {lang}: {e}")
                success = False
        return success

    def ask_question(self, question_details: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        required_keys = ["history", "user_question", "project_id", "lang", "company_data", "project_name"]
        for key in required_keys:
            if key not in question_details:
                return {"error": f"Missing key: {key}"}

        try:
            q_texts = contextualize_question(
                chat_history=question_details["history"],
                latest_question=question_details["user_question"],
                project_name=question_details["project_name"],
                lang=question_details["lang"],
                agent_type = question_details["service_type"]
            )
            q_texts.append(question_details["user_question"])
            context = [
                self.query_core_data(
                    query=q,
                    lang=question_details["lang"],
                    project_id=question_details["project_id"]
                ) for q in q_texts if q
            ]

            response = answer_question({
                "context": context,
                "reformulations": q_texts,
                "user_question": question_details["user_question"],
                "project_id": question_details["project_id"],
                "project_name": question_details["project_name"],
                "lang": question_details["lang"],
                "history": question_details["history"],
                "company_data": question_details["company_data"],
                "service_type": question_details["service_type"]
            })

            return response

        except Exception as e:
            self.logger.error(f"QA failed: {e}")
            return {"error": str(e), "processing_time": time.time() - start}
