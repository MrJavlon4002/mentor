from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from document_handler import DocumentHandler
from enum import Enum
from typing import Any

app = FastAPI()
handler = DocumentHandler()

# -----------------------------
# Middleware for Token Check
# -----------------------------

base_token = "Bearer a1b2c3"

@app.middleware("http")
async def token_check_middleware(request: Request, call_next):
    # Endpoints to skip token check
    skip_paths = []
    if request.url.path in skip_paths:
        return await call_next(request)

    # Token validation
    token = request.headers.get("authorization")
    if not token or token != base_token:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or missing token"},
        )
    return await call_next(request)

# -----------------------------
# Pydantic Models
# -----------------------------

class ProductCreateRequest(BaseModel):
    details: Dict
    project_id: str
    lang: str

class ProductGetRequest(BaseModel):
    project_id: str
    product_id: str
    languages: List[str]

class ProductUpdateRequest(BaseModel):
    project_id: str
    product_id: str
    details: Dict

class ProductDeleteRequest(BaseModel):
    project_id: str
    product_id: str
    languages: List[str]

class ServiceType(str, Enum):
    sales = 'sales'
    support = 'support'
    staff = 'staff'
    qa = 'q/a'

class AskQuestionRequest(BaseModel):
    project_id: str
    project_name: str
    user_question: str
    history: list[dict[str, Any]] = []
    lang: str
    company_data: Optional[str] = ""
    service_type: ServiceType

class DeleteProjectRequest(BaseModel):
    project_id: str
    languages: List[str]

class DataUploadRequest(BaseModel):
    project_id: str
    row_data: str
    languages: List[str]

# -----------------------------
# Endpoints
# -----------------------------

@app.post("/products")
async def create_product(request: ProductCreateRequest):
    try:
        handler.create_product(
            details=request.details,
            project_id=request.project_id,
            lang=request.lang
        )
        return {"status": "success", "message": f"Product created for project '{request.project_id}'."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.get("/products/{product_id}")
async def get_product(project_id: str, product_id: str, languages: List[str]):
    try:
        product = handler.get_product(
            project_id=project_id,
            product_id=product_id,
            languages=languages
        )
        if product == "Product not found in any language.":
            return JSONResponse(status_code=404, content={"detail": product})
        return {"status": "success", "product": product}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.get("/products")
async def get_all_products(project_id: str, languages: List[str]):
    try:
        products = handler.get_all_products(
            project_id=project_id,
            languages=languages
        )
        if products == "No products found in any language.":
            return JSONResponse(status_code=404, content={"detail": products})
        return {"status": "success", "products": products}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.put("/products/{product_id}")
async def update_product(product_id: str, request: ProductUpdateRequest):
    try:
        handler.update_product(
            project_id=request.project_id,
            product_id=product_id,
            details=request.details
        )
        return {"status": "success", "message": f"Product '{product_id}' updated."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.delete("/products/{product_id}")
async def delete_product(product_id: str, project_id: str, languages: List[str]):
    try:
        success = handler.delete_product(
            project_id=project_id,
            product_id=product_id,
            languages=languages
        )
        if success:
            return {"status": "success", "message": f"Product '{product_id}' deleted."}
        return JSONResponse(status_code=400, content={"detail": "Failed to delete product."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/ask_question")
async def ask_question(request: AskQuestionRequest):
    try:
        question_details = {
            "project_id": request.project_id,
            "project_name": request.project_name,
            "history": request.history,
            "user_question": request.user_question,
            "lang": request.lang,
            "company_data": request.company_data,
            "service_type": request.service_type
        }
        answer = handler.ask_question(question_details=question_details)
        return {"status": "success", "answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    
@app.delete("/delete_project")
async def delete_project(request: DeleteProjectRequest):
    try:
        handler.delete_project(
            project_id=request.project_id,
            languages=request.languages
        )
        return {"status": "success", "message": f"Project '{request.project_id}' deleted successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/data_upload")
async def data_upload(request: DataUploadRequest):
    try:
        handler.data_upload(
            project_id=request.project_id,
            row_data=request.row_data,
            languages=request.languages
        )
        return {"status": "success", "message": "Data uploaded successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    
@app.post("/delete_all")
async def delete_all():
    try:
        handler.delete_all()
        return {"status": "success", "message": "All data deleted successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
