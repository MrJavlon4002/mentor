import weaviate
from weaviate.classes.config import Configure
import api_keys

class WeaviateDatabase:
    def __init__(self):
        self.headers = {"X-VoyageAI-Api-Key": api_keys.VOYAGE_API_KEY}

    def _create_client(self):
        return weaviate.connect_to_local(host="weaviate", port=8080, headers=self.headers)

    def initialize_and_insert_data(self, row_data, project_id: str):
        
        with self._create_client() as client:
            # client.collections.delete_all()
            # print("Existing collections deleted.")
            for lang, chunks in row_data.items():
                project_id_lang = f"{project_id}_{lang}"
                self._ensure_collection_exists(client, project_id_lang)

                collection = client.collections.get(project_id_lang)

                with collection.batch.dynamic() as batch:
                    for idx, chunk_data in enumerate(chunks.values()):

                        print("=== ", chunks, " ===", lang)
                        batch.add_object(

                            properties={
                                "title": chunk_data["title"],
                                "text": chunk_data["text"],
                                "number": idx,
                            }
                        )

                        if batch.number_errors > 10:
                            print("Batch import stopped due to excessive errors.")
                            break

                print(f"Inserted data into collection '{project_id_lang}'.")

                
    def _ensure_collection_exists(self, client, project_id):
        if not client.collections.exists(project_id):
            client.collections.create(
                project_id,
                vectorizer_config=[
                    Configure.NamedVectors.text2vec_voyageai(
                        name="text_vector",
                        source_properties=["text", "title"],
                        model="voyage-3",
                    ),
                ]
            )
            print(f"Collection '{project_id}' created with VoyageAI vectorizer.")
        else:
            print(f"Collection '{project_id}' already exists.")
    
    def delete_project(self, project_id: str, language: str = None):
        
        with self._create_client() as client:
            collections = client.collections.list_all()
            if not collections:
                print("No collections found.")
                return False
            
            if language:
                project_id = f"{project_id}_{language}"
                if client.collections.exists(project_id):
                    client.collections.delete(project_id)
                    print(f"Collection '{project_id}' deleted.")
                    return True
                print(f"Collection '{project_id}' does not exist.")
                return False
            else:
                deleted = False
                for collection in collections:
                    if collection.name.startswith(f"{project_id}_"):
                        client.collections.delete(collection.name)
                        print(f"Collection '{collection.name}' deleted.")
                        deleted = True
                return deleted
                

    def check_collection(self, project_id: str):
        
        with self._create_client() as client:
            collections = client.collections.list_all()
            if not collections:
                print("No collections found.")
                return False
            for collection in collections:
                if collection.name == project_id:
                    print(f"Collection '{project_id}' exists.")
                    return True
            print(f"Collection '{project_id}' does not exist.")
            return False
    

    def add_product(self, project_id: str, details: dict):
        """Adds a product to the vector database."""
        
        with self._create_client() as client:
            if not client.collections.exists(project_id):
                print(f"Collection '{project_id}' does not exist.")
                return False

            try:
                collection = client.collections.get(project_id)
                with collection.batch.dynamic() as batch:
                    batch.add_object(
                        properties={
                            "name": details["name"],
                            "details": details["details"]
                        },
                        uuid=details["id"],
                    )
                print(f"Product added to collection '{project_id}'.")
                return True
            except Exception as e:
                print(f"Error adding product: {e}")
                return False
            finally:
                client.close()
    
    def get_product(self, project_id: str, product_id: str, ):
        """Retrieves a product from the vector database."""
        
        with self._create_client() as client:
            if not client.collections.exists(project_id):
                print(f"Collection '{project_id}' does not exist.")
                return None

            collection = client.collections.get(project_id)
            try:
                response = collection.query.fetch_object_by_id(product_id)
                if response:
                    return response.properties
                else:
                    print(f"Product with ID '{product_id}' not found in collection '{project_id}'.")
                    return None
            except Exception as e:
                print(f"Error retrieving product: {e}")
                return None
            finally:
                client.close()

    def get_all_product(self, project_id: str):
        """Retrieves a product from the vector database."""
        with self._create_client() as client:
            if not client.collections.exists(project_id):
                print(f"Collection '{project_id}' does not exist.")
                return None

            collection = client.collections.get(project_id)
            try:
                all_products = []
                for item in collection.iterator():
                    all_products.append(item.properties)
                return all_products
            except Exception as e:
                print(f"Error retrieving products: {e}")
                return None
            finally:
                client.close()

    
    def update_product(self, project_id: str, details: dict):
        """Updates a product in the vector database."""

        with self._create_client() as client:
            if not client.collections.exists(project_id):
                print(f"Collection '{project_id}' does not exist.")
                return False

            collection = client.collections.get(project_id)
            try:
                collection.data.update(
                    uuid=details['id'],
                    properties={
                        "name": details['name'],
                        "details": details['details']
                    },
                )
                print(f"Product with ID '{details['id']}' updated in collection '{project_id}'.")
                return True
            except Exception as e:
                print(f"Error updating product: {e}")
                return False
            finally:
                client.close()

    def delete_product(self, project_id: str, product_id: str):
        """Deletes a product from the vector database."""
        
        with self._create_client() as client:
            if not client.collections.exists(project_id):
                print(f"Collection '{project_id}' does not exist.")
                return False

            collection = client.collections.get(project_id)
            try:
                collection.data.delete_by_id(product_id)
                print(f"Product with ID '{product_id}' deleted from collection '{project_id}'.")
            except Exception as e:
                print(f"Error deleting product: {e}")
                return False
            finally:
                client.close()


    def hybrid_query(self, query: str, project_id, limit=3):
        client = None
        try:
            client = self._create_client()
            if not client.collections.exists(project_id):
                print(f"Collection '{project_id}' not found.")
                return []

            collection = client.collections.get(project_id)
            if isinstance(query, list): 
                query = ' '.join(query)

            response = collection.query.hybrid(
                query=query,
                limit=limit,
                alpha=0.7,
            )
            return [{
                'text': obj.properties.get('text', ''),
                'title': obj.properties.get('title', ''),
                'name': obj.properties.get('name', ''),
                'details': obj.properties.get('details', ''),
                'id': obj.uuid,
            } for obj in response.objects]


        except Exception as e:
            print(f"Error during query: {e}")
            return []
        finally:
            if client:
                client.close()