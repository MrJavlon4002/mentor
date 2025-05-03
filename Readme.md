# Vector Database API

This project provides a FastAPI-based API for managing products in a vector database, supporting multilingual product data, data uploads, and question-answering capabilities. The API allows users to create, retrieve, update, delete products, upload text data, and ask questions based on stored data.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Usage Example](#usage-example)
- [Notes](#notes)

## Project Structure

Below is the structure of the project directory:

```
├── __pycache__             # Compiled Python bytecode
├── api_keys.py             # API key configurations
├── app.py                  # FastAPI application with endpoint definitions
├── data                    # Directory for data storage
├── data_prep               # Data preparation scripts
├── database                # Database-related scripts
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration for the application
├── document_hendler.py     # Core logic for handling documents and vector database operations
├── general                 # General utility scripts
├── main.py                 # Entry point for running the application
├── requirements.txt        # Python dependencies
└── Readme.md               # Project documentation
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up API keys**:
   Configure necessary API keys in `api_keys.py` for external services (e.g., translation or database access).

3. **Build and run with Docker Compose**:
   Ensure Docker and Docker Compose are installed. Build and start the services defined in `docker-compose.yml`:
   ```bash
   docker-compose up --build -d
   ```

4. **Access the API**:
   The API will be available at `http://localhost:8000`. Explore the interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

The endpoints are defined in `app.py` and leverage the `DocumentHandler` class from `document_hendler.py` for vector database operations. Below are the available endpoints with cURL commands using generic placeholders.

### 1. Data Upload
**Description**: Uploads text data to the vector database for a specified project and languages.

**cURL Command**:
```bash
curl -X POST "http://localhost:8000/data_taking" \
-H "Content-Type: application/json" \
-d '{
    "text": "<text>",
    "project": "<project_id>",
    "languages": ["<lang1>", "<lang2>"]
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "message": "Data inserted successfully."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 2. Create a Product
**Description**: Creates a new product in the vector database for a specified project and language.

**cURL Command**:
```bash
curl -X POST "http://localhost:8000/products" \
-H "Content-Type: application/json" \
-d '{
    "details": {
        "name": "<product_name>",
        "description": "<product_description>",
        "price": "<product_price>",
        "id": "<product_id>",
        "languages": ["<lang1>", "<lang2>"]
    },
    "project_id": "<project_id>",
    "lang": "<lang>"
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "message": "Product created for project '<project_id>'."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 3. Get a Product
**Description**: Retrieves a specific product by ID from the vector database for the specified languages.

**cURL Command**:
```bash
curl -X GET "http://localhost:8000/products/<product_id>" \
-H "Content-Type: application/json" \
-d '{
    "project_id": "<project_id>",
    "product_id": "<product_id>",
    "languages": ["<lang1>", "<lang2>"]
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "product": {"<lang>": {"name": "<product_name>", "description": "...", "price": "<product_price>", "id": "<product_id>", "languages": ["<lang1>", "<lang2>"]}}}`
- **404 Not Found**: `{"detail": "Product not found in any language."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 4. Get All Products
**Description**: Retrieves all products for a specified project and languages.

**cURL Command**:
```bash
curl -X GET "http://localhost:8000/products?project_id=<project_id>&languages=<lang1>&languages=<lang2>" \
-H "Content-Type: application/json"
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "products": {"<lang>": [{"name": "<product_name>", "description": "...", "price": "<product_price>", "id": "<product_id>", "languages": ["<lang1>", "<lang2>"]}, ...]}}`
- **404 Not Found**: `{"detail": "No products found in any language."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 5. Delete a Product
**Description**: Deletes a product by ID from the vector database for the specified languages.

**cURL Command**:
```bash
curl -X DELETE "http://localhost:8000/products/<product_id>" \
-H "Content-Type: application/json" \
-d '{
    "project_id": "<project_id>",
    "product_id": "<product_id>",
    "languages": ["<lang1>", "<lang2>"]
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "message": "Product '<product_id>' deleted."}`
- **400 Bad Request**: `{"detail": "Failed to delete product."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 6. Ask a Question
**Description**: Handles user queries by fetching relevant data and generating a response.

**cURL Command**:
```bash
curl -X POST "http://localhost:8000/ask_question" \
-H "Content-Type: application/json" \
-d '{
    "project_id": "<project_id>",
    "project_name": "<project_name>",
    "user_question": "<question>",
    "history": ["<previous_question>"],
    "lang": "<lang>",
    "company_data": "<company_info>"
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "answer": "..."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

## Usage Example

The following sequence demonstrates how to use the API with placeholder values:

1. **Upload Data**:
   ```bash
   curl -X POST "http://localhost:8000/data_taking" \
   -H "Content-Type: application/json" \
   -d '{
       "text": "<company_and_course_info>",
       "project": "<project_id>",
       "languages": ["<lang1>", "<lang2>"]
   }'
   ```

2. **Create a Product**:
   ```bash
   curl -X POST "http://localhost:8000/products" \
   -H "Content-Type: application/json" \
   -d '{
       "details": {
           "name": "<course_name>",
           "description": "<course_description>",
           "price": "<course_price>",
           "id": "<unique_id>",
           "languages": ["<lang1>", "<lang2>"]
       },
       "project_id": "<project_id>",
       "lang": "<lang1>"
   }'
   ```

3. **Get a Product**:
   ```bash
   curl -X GET "http://localhost:8000/products/<unique_id>" \
   -H "Content-Type: application/json" \
   -d '{
       "project_id": "<project_id>",
       "product_id": "<unique_id>",
       "languages": ["<lang1>", "<lang2>"]
   }'
   ```

4. **Delete a Product**:
   ```bash
   curl -X DELETE "http://localhost:8000/products/<unique_id>" \
   -H "Content-Type: application/json" \
   -d '{
       "project_id": "<project_id>",
       "product_id": "<unique_id>",
       "languages": ["<lang1>", "<lang2>"]
   }'
   ```

5. **Ask a Question**:
   ```bash
   curl -X POST "http://localhost:8000/ask_question" \
   -H "Content-Type: application/json" \
   -d '{
       "project_id": "<project_id>",
       "project_name": "<project_name>",
       "user_question": "<question>",
       "history": [],
       "lang": "<lang1>",
       "company_data": "<company_info>"
   }'
   ```

## Notes
- Replace placeholders (e.g., `<project_id>`, `<product_id>`, `<text>`) with actual values specific to your use case.
- Ensure the `Content-Type: application/json` header is included for POST, PUT, and DELETE requests.
- For generating unique IDs (e.g., `<product_id>`), use a UUID generator like `uuidgen` on Unix systems or a similar tool.
- For troubleshooting, check the interactive API documentation at `http://localhost:8000/docs` or view container logs with `docker-compose logs`.