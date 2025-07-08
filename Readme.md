# 🧠 Mentour Product & Knowledge API

A FastAPI-based multilingual product and Q&A platform. This API enables CRUD operations on multilingual products and contextual Q&A functionality for structured project data.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mentor.git
cd mentor
2. Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
3. Run the app
uvicorn app:app --reload
🛡️ Security

By default, the IP whitelist middleware is disabled. To enable:
Uncomment the line in your app startup:

# app.add_middleware(IPWhitelistMiddleware)
Then add allowed IPs to the ALLOWED_IPS set.

📚 API Documentation

Once running, access Swagger UI at:

http://127.0.0.1:8000/docs
📦 Endpoints

🔹 POST /products — Create Product
Create a multilingual product for a project.

Request body:

{
  "details": { "id": "123", "name": "Test", "details": { "desc": "Example" } },
  "project_id": "example",
  "lang": "en"
}
🔹 GET /products/{product_id} — Get Product Details
Retrieve a product across specified languages.

Query params:

project_id: string
languages: comma-separated list of language codes (e.g. en,ru)
🔹 GET /products — List All Products
List all products of a project across multiple languages.

Query params:

project_id: string
languages: comma-separated list
🔹 PUT /products/{product_id} — Update Product
Update product details across all languages.

Request body:

{
  "project_id": "example",
  "product_id": "123",
  "details": {
    "id": "123",
    "name": "Updated Name",
    "details": { "desc": "New description" }
  }
}
🔹 DELETE /products/{product_id} — Delete Product
Remove a product in specified languages.

Query params:

project_id: string
languages: comma-separated list
🔹 POST /ask_question — Ask Contextual Question
Ask questions using project context, history, and service type.

Request body:

{
  "project_id": "example",
  "project_name": "Example Project",
  "user_question": "What is this product about?",
  "history": [],
  "lang": "en",
  "company_data": "Additional context …",
  "service_type": "support"
}
📌 service_type must be one of:
sales / support / staff / q/a

🔹 DELETE /delete_project — Delete Entire Project
Delete all data tied to a project.

Request body:

{
  "project_id": "example",
  "languages": ["en","ru"]
}
🔹 POST /data_upload — Upload Raw Data
Upload raw or tabular project data for indexing.

Request body:

{
  "project_id": "example",
  "row_data": "Some tabular data here",
  "languages": ["en","ru"]
}
🔹 POST /delete_all — Clear Entire Database
Wipe all stored data across every project and language.

🧠 Notes

Question answering and translations use an LLM via call_llm_with_functions.
Data is stored per-language under keys like project_id_<lang> in the vector store.
📂 Project Structure

.
├── app.py                 # FastAPI application  
├── document_handler.py   # Core product & QA business logic  
├── data_prep/            # Data preparation utilities  
├── database/             # Vector database integrations  
├── general/              # LLM helper utilities  
├── Dockerfile  
├── docker-compose.yml  
├── nginx.conf  
├── requirements.txt  
└── README.md             # ← you’re here  
📫 Contact

Need help or want to collaborate? Reach me at:
valiyevjavlon001@gmail.com