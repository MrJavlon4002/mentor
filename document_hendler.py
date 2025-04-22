import time
from database.vector_database import WeaviateDatabase
from general.gemini_llm import contextualize_question, answer_question
from data_prep.data_preparation import prepare_data

class DocumentHandler:
    def __init__(self):
        """Initializes the document handler with a vector database client and prepares the database."""
        self.client = WeaviateDatabase()

    def data_upload(self, project_name, row_data, languages: list = ['uz', 'ru']):
        """Initializes the vector database and inserts data."""
        processed_data = prepare_data(row_data, languages)
        self.client.initialize_and_insert_data(processed_data, project_name=project_name)
        print("Data insertion complete.")

    def query_core_data(self,project_name :str, query: str, lang: str) -> str:
        """Queries the database for relevant information."""
        results = self.client.hybrid_query(query=query, collection_name=f"{project_name}_{lang}")
        return results if results else "No relevant data found."

    def ask_question(self, history: list, user_input: str, project_name: str, lang: str):
        """Handles user queries by contextualizing the question, fetching relevant data, and generating a response."""
        start_time = time.time()

        # Contextualize question
        standalone_questions = contextualize_question(
            history, 
            user_input, 
            project_name=project_name
        )

        context = [
            self.query_core_data(query=question, lang=lang, project_name=project_name)
            for question in standalone_questions["text"] if question
        ]
        full_response = answer_question(context, standalone_questions["text"], user_input, project_name=project_name, chat_history=history, lang=lang)
        
        

        print(f"Total processing time: {time.time() - start_time:.2f} seconds")
        
        return full_response
