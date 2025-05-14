Here is a complete `README.md` for your FastAPI project, including setup instructions and documentation for all available endpoints:

---

````markdown
# 🧠 IZI-NLP Product & Knowledge API

A FastAPI-based multilingual product and Q&A platform. This API allows you to create, update, retrieve, delete products across multiple languages, as well as ask questions using contextual project data.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/izi-nlp.git
cd izi-nlp
````

### 2. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the app

```bash
uvicorn main:app --reload
```

---

## 🛡️ Security

> By default, the IP whitelist middleware is **disabled**. To enable:

Uncomment:

```python
# app.add_middleware(IPWhitelistMiddleware)
```

Add allowed IPs to the `ALLOWED_IPS` set.

---

## 📚 API Documentation

> Once running, access **Swagger UI** at:
> [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📦 Endpoints

### 🔹 `POST /products` — Create Product

Create a multilingual product from a base language.

**Request body:**

```json
{
  "details": { "id": "123", "name": "Test", "details": { "desc": "Example" }, "languages": ["en", "ru"] },
  "project_id": "osnova",
  "lang": "en"
}
```

---

### 🔹 `GET /products/{product_id}` — Get Product

Fetch a product in all specified languages.

**Query params:**

* `project_id`: string
* `languages`: list of language codes (e.g. `en,ru`)

---

### 🔹 `GET /products` — Get All Products

List all products for a project in multiple languages.

**Query params:**

* `project_id`: string
* `languages`: list of language codes

---

### 🔹 `PUT /products/{product_id}` — Update Product

Update a product in all its languages.

**Request body:**

```json
{
  "project_id": "osnova",
  "product_id": "123",
  "details": {
    "id": "123",
    "name": "Updated Name",
    "details": { "desc": "Updated description" },
    "languages": ["en", "ru"]
  }
}
```

---

### 🔹 `DELETE /products/{product_id}` — Delete Product

Delete a product across multiple languages.

**Query params:**

* `project_id`: string
* `languages`: list of language codes

---

### 🔹 `POST /ask_question` — Ask Question

Ask a question about project-specific content with history.

**Request body:**

```json
{
  "project_id": "osnova",
  "project_name": "Osnova Q&A",
  "user_question": "What is this product about?",
  "lang": "en",
  "history": [],
  "company_data": "...",
  "service_type": "",
}
```
service_types => 'sales' / 'support' / 'staff' / 'q/a'

---

### 🔹 `DELETE /delete_project` — Delete Entire Project

Deletes all product data associated with a project.

**Request body:**

```json
{
  "project_id": "osnova",
  "languages": ["en", "ru"]
}
```

---

### 🔹 `POST /data_upload` — Upload Raw Data

Used for uploading structured row data into a project.

**Request body:**

```json
{
  "project_id": "osnova",
  "row_data": "Some tabular data here",
  "languages": ["en", "ru"]
}
```

---

## 🧠 Notes

* Translations are powered by an LLM (via `call_llm_with_functions`)
* Product content is always stored per-language: `project_id_<lang>`

---

## 📂 Project Structure

```
.
├── main.py               # FastAPI app
├── document_handler.py   # Product and QA logic
├── requirements.txt
└── README.md             # ← you are here
```

---

## 📫 Contact

For support or collaboration, reach out at:
`valiyevjavlon001@gmail.com`

---

```

Let me know if you want to include `example curl` commands or add authentication support.
```
