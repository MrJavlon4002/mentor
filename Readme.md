# Vector Database API

This project provides a FastAPI-based API for managing products in a vector database, supporting multilingual product data, data uploads, and question-answering capabilities. The API allows users to create, retrieve, update, and delete products, upload text data, and ask questions based on the stored data.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
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
   Ensure Docker and Docker Compose are installed. Then, build and start the services defined in `docker-compose.yml`:
   ```bash
   docker-compose up --build -d
   ```

4. **Access the API**:
   The API will be available at `http://localhost:8000`. Explore the interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

The endpoints are defined in `app.py` and leverage the `DocumentHandler` class from `document_hendler.py` for vector database operations. Below are the available endpoints with cURL commands.

### 1. Create a Product
**Description**: Creates a new product in the vector database for a specified project and language.

**cURL Command**:
```bash
curl -X POST "http://localhost:8000/products" \
-H "Content-Type: application/json" \
-d '{
    "details": {"name": "Sample Product", "description": "A sample product", "languages": ["en", "es"]},
    "project_name": "test_project",
    "lang": "en"
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "message": "Product created for project 'test_project'."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 2. Get a Product
**Description**: Retrieves a specific product by ID from the vector database for the specified languages.

**cURL Command**:
```bash
curl -X GET "http://localhost:8000/products/sample_product_id" \
-H "Content-Type: application/json" \
-d '{
    "project_name": "test_project",
    "product_id": "sample_product_id",
    "languages": ["en", "es"]
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "product": {...}}`
- **404 Not Found**: `{"detail": "Product not found in any language."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 3. Get All Products
**Description**: Retrieves all products for a specified project and languages.

**cURL Command**:
```bash
curl -X GET "http://localhost:8000/products?project_name=test_project&languages=en&languages=es" \
-H "Content-Type: application/json"
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "products": {...}}`
- **404 Not Found**: `{"detail": "No products found in any language."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 4. Update a Product
**Description**: Updates an existing product in the vector database.

**cURL Command**:
```bash
curl -X PUT "http://localhost:8000/products/sample_product_id" \
-H "Content-Type: application/json" \
-d '{
    "project_name": "test_project",
    "product_id": "sample_product_id",
    "details": {"name": "Updated Product", "description": "Updated description", "languages": ["en", "es"]}
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "message": "Product 'sample_product_id' updated."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 5. Delete a Product
**Description**: Deletes a product by ID from the vector database for the specified languages.

**cURL Command**:
```bash
curl -X DELETE "http://localhost:8000/products/sample_product_id" \
-H "Content-Type: application/json" \
-d '{
    "project_name": "test_project",
    "product_id": "sample_product_id",
    "languages": ["en", "es"]
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "message": "Product 'sample_product_id' deleted."}`
- **400 Bad Request**: `{"detail": "Failed to delete product."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 6. Ask a Question
**Description**: Handles user queries by fetching relevant data and generating a response.

**cURL Command**:
```bash
curl -X POST "http://localhost:8000/ask_question" \
-H "Content-Type: application/json" \
-d '{
    "project_name": "test_project",
    "user_question": "What is the product description?",
    "history": ["Previous question"],
    "lang": "en",
    "company_data": {"company_name": "Test Inc"}
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "answer": "..."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

### 7. Data Upload
**Description**: Uploads text data to the vector database for a specified project and languages.

**cURL Command**:
```bash
curl -X POST "http://localhost:8000/data_taking" \
-H "Content-Type: application/json" \
-d '{
    "text": "Sample text data",
    "project": "test_project",
    "languages": ["en", "es"]
}'
```

**Expected Responses**:
- **200 OK**: `{"status": "success", "message": "Data inserted successfully."}`
- **500 Internal Server Error**: `{"detail": "Error message"}`

## Usage

To interact with the API:
1. Ensure the Docker containers are running (`docker-compose up --build -d`).
2. Use the cURL commands above or tools like Postman to send requests.
3. Replace `sample_product_id` and `test_project` with actual values from your database.
4. For multilingual support, specify the desired languages in the `languages` field.

## Notes
- Replace `http://localhost:8000` with the actual server URL if deployed.
- Ensure the `Content-Type: application/json` header is included for POST, PUT, and DELETE requests.
- The `product_id` and `project_name` in the examples should be replaced with actual values from your database.
- For troubleshooting, check the interactive API documentation at `http://localhost:8000/docs` or view container logs with `docker-compose logs`.