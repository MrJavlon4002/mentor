import time
from database.vector_database import WeaviateDatabase
from general.gemini_llm import contextualize_question, answer_question
from data_prep.data_preparation import prepare_data
from data_prep.data_preparation import language_detection
from data_prep.tahrirchi import translate_text

class DocumentHandler:
    def __init__(self):
        """Initializes the document handler with a vector database client and prepares the database."""
        self.client = WeaviateDatabase()

    def data_upload(self, project_name, row_data, languages: list = ['uz', 'ru']):
        """Initializes the vector database and inserts data."""
        processed_data = prepare_data(row_data, languages)
        self.client.initialize_and_insert_data(processed_data, project_name=project_name)
        print("Data insertion complete.")



    # Create a product in the vector database
    def create_product(self, details: dict, project_name: str, lang: str,):
        """Creates a product in the vector database."""
        source_lang = language_detection(str(details['description']))
        translated_data = {}
        translated_data[source_lang] = details
        
        for lang in details['languages']:
            if lang != source_lang:
                # time.sleep(1.3)
                translated = {}
                for key, value in details.items():
                    if key == 'description':
                        translated[key] = translate_text(str(value), source_lang, lang)
                    else:
                        translated[key] = value
                translated_data[lang] = translated
            
            self.client.add_product(project_name=f"{project_name}_{lang}", details=translated_data[lang])
            print(f"Product created for language '{lang}'.")

    
    # Get a product from the vector database
    def get_product(self, project_name: str, product_id: str, languages: list):

        """Retrieves a product from the vector database."""
        product = {}
        for lang in languages:
            product[lang] = self.client.get_product(project_name=f"{project_name}_{lang}", product_id=product_id)
            if product[lang]:
                print(f"Product found in language '{lang}'.")
        return product[lang] if product[lang] else "Product not found in any language."
    
    # Get all products from the vector database
    def get_all_products(self, project_name: str, languages: list):
        """Retrieves all products from the vector database."""
        products = {}
        for lang in languages:
            products[lang] = self.client.get_all_products(project_name=f"{project_name}_{lang}")
            if products[lang]:
                print(f"Products found in language '{lang}'.")
        return products[lang] if products[lang] else "No products found in any language."
    
    # Update a product in the vector database
    def update_product(self, project_name: str, product_id: str, details: dict):
        """Updates a product in the vector database."""

        for lang in details['languages']:
            if lang != details['languages'][0]:
                # time.sleep(1.3)
                translated = {}
                for key, value in details.items():
                    if key == 'description':
                        translated[key] = translate_text(str(value), details['languages'][0], lang)
                    else:
                        translated[key] = value
                details[lang] = translated
            
            self.client.update_product(project_name=f"{project_name}_{lang}", product_id=product_id, details=details[lang])
            print(f"Product updated for language '{lang}'.")

    # Delete a product from the vector database
    def delete_product(self, project_name: str, product_id: str, languages: list):
        """Deletes a product from the vector database."""
        for lang in languages:
            self.client.delete_product(project_name=f"{project_name}_{lang}", product_id=product_id)
            print(f"Product with ID '{product_id}' deleted from project '{project_name}_{lang}'.")
        return True




    # Search for a product in the vector database
    def query_core_data(self, project_name: str, query: str, lang: str) -> str:
        """Queries the database for relevant information."""
        results = self.client.hybrid_query(query=query, collection_name=f"{project_name}_{lang}")
        return results if results else "No relevant data found."
    

    # Answering the question
    def ask_question(self, question_details: dict):
        """Handles user queries by contextualizing the question, fetching relevant data, and generating a response."""
        start_time = time.time()


        history = question_details["history"]
        user_question = question_details["user_question"]
        project_name = question_details["project_name"]
        lang = question_details["lang"]
        company_data = question_details["company_data"]

        # Contextualize question
        standalone_questions = contextualize_question(
             chat_history=history, 
             latest_question=user_question, 
             project_name= project_name,
        )

        # Taking data from verctor database
        context = [
            self.query_core_data(query=question, lang=lang, project_name=project_name)
            for question in standalone_questions["text"] if question
        ]



        # Answering the question
        details_for_response = {
            "context": context,
            "reformulations": standalone_questions["text"],
            "user_question": user_question,
            "project_name": project_name,
            "lang": lang,
            "history": history,
            "company_data": company_data
        }

        full_response = answer_question(details_for_response)
        
        

        print(f"Total processing time: {time.time() - start_time:.2f} seconds")
        
        return full_response
