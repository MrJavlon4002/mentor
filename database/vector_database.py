import weaviate
from weaviate.classes.config import Configure, Property, DataType
import api_keys

class WeaviateDatabase:
    def __init__(self):
        self.headers = {"X-VoyageAI-Api-Key": api_keys.VOYAGE_API_KEY}

    def _create_client(self):
        return weaviate.connect_to_local(host="localhost", port=8080, headers=self.headers)

    def initialize_and_insert_data(self, row_data, project_name: str):
        project_name = project_name.lower()
        with self._create_client() as client:
            client.collections.delete_all()
            print("Existing collections deleted.")

            for lang, chunks in row_data.items():
                collection_name = f"{project_name}_{lang}"
                self._ensure_collection_exists(client, collection_name)

                collection = client.collections.get(collection_name)

                with collection.batch.dynamic() as batch:
                    for idx, chunk_data in enumerate(chunks.values()):
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

                print(f"Inserted data into collection '{collection_name}'.")

    def _ensure_collection_exists(self, client, collection_name):
        if not client.collections.exists(collection_name):
            client.collections.create(
                collection_name,
                properties=[
                    Property(name="title", data_type=DataType.TEXT, index_searchable=True),
                    Property(name="text", data_type=DataType.TEXT, index_searchable=True),
                    Property(name="number", data_type=DataType.INT),
                ],
                vectorizer_config=[
                    Configure.NamedVectors.text2vec_voyageai(
                        name="text_vector",
                        source_properties=["text", "title"],
                        model="voyage-3",
                    ),
                ]
            )
            print(f"Collection '{collection_name}' created with VoyageAI vectorizer.")
        else:
            print(f"Collection '{collection_name}' already exists.")



    def hybrid_query(self, query: str, collection_name, limit=3):
        client = None
        try:
            client = self._create_client()
            if not client.collections.exists(collection_name):
                print(client.collections.list_all())
                print(f"Collection '{collection_name}' not found.")
                return []

            collection = client.collections.get(collection_name)
            if isinstance(query, list): 
                query = ' '.join(query)

            response = collection.query.hybrid(
                query=query,
                limit=limit,
                alpha=1,
                query_properties=["text", "title", "number"]
            )
            return [{
                'text': obj.properties.get('text', ''),
                'title': obj.properties.get('title', ''),
                'number': obj.properties.get('number', '')
            } for obj in response.objects]

        except Exception as e:
            print(f"Error during query: {e}")
            return []
        finally:
            if client:
                client.close()

