from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from document_handler import DocumentHandler
from enum import Enum

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI()
handler = DocumentHandler()

# Rate Limiter Setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# -----------------------------
# Token Check Middleware
# -----------------------------
base_token = "Bearer a1b2c3"

@app.middleware("http")
async def token_check_middleware(request: Request, call_next):
    skip_paths = []
    if request.url.path in skip_paths:
        return await call_next(request)

    token = request.headers.get("authorization")
    if not token or token != base_token:
        return JSONResponse(status_code=401, content={"detail": "Invalid or missing token"})

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
# Endpoints with Rate Limits
# -----------------------------

# /products (POST)
@limiter.limit("10/minute")
@app.post("/products")
async def create_product(request: ProductCreateRequest):
    try:
        handler.create_product(request.details, request.project_id, request.lang)
        return {"status": "success", "message": f"Product created for project '{request.project_id}'."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# /products/{product_id} (GET)
@limiter.limit("60/minute")
@app.get("/products/{product_id}")
async def get_product(project_id: str, product_id: str, languages: List[str]):
    try:
        product = handler.get_product(project_id, product_id, languages)
        if product == "Product not found in any language.":
            return JSONResponse(status_code=404, content={"detail": product})
        return {"status": "success", "product": product}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# /products (GET)
@limiter.limit("60/minute")
@app.get("/products")
async def get_all_products(project_id: str, languages: List[str]):
    try:
        products = handler.get_all_products(project_id, languages)
        if products == "No products found in any language.":
            return JSONResponse(status_code=404, content={"detail": products})
        return {"status": "success", "products": products}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# /products/{product_id} (PUT)
@limiter.limit("10/minute")
@app.put("/products/{product_id}")
async def update_product(product_id: str, request: ProductUpdateRequest):
    try:
        handler.update_product(request.project_id, product_id, request.details)
        return {"status": "success", "message": f"Product '{product_id}' updated."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# /products/{product_id} (DELETE)
@limiter.limit("5/minute")
@app.delete("/products/{product_id}")
async def delete_product(product_id: str, project_id: str, languages: List[str]):
    try:
        success = handler.delete_product(project_id, product_id, languages)
        if success:
            return {"status": "success", "message": f"Product '{product_id}' deleted."}
        return JSONResponse(status_code=400, content={"detail": "Failed to delete product."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# /ask_question (POST)
@limiter.limit("15/minute")
@app.post("/ask_question")
async def ask_question(request: AskQuestionRequest):
    try:
        answer = await handler.ask_question({
            "project_id": request.project_id,
            "project_name": request.project_name,
            "history": request.history,
            "user_question": request.user_question,
            "lang": request.lang,
            "company_data": request.company_data,
            "service_type": request.service_type
        })
        return {"status": "success", "answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# /delete_project (DELETE)
@limiter.limit("2/minute")
@app.delete("/delete_project")
async def delete_project(request: DeleteProjectRequest):
    try:
        handler.delete_project(request.project_id, request.languages)
        return {"status": "success", "message": f"Project '{request.project_id}' deleted successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# /data_upload (POST)
@limiter.limit("8/minute")
@app.post("/data_upload")
async def data_upload(request: DataUploadRequest):
    try:
        await handler.data_upload(request.project_id, request.row_data, request.languages)
        return {"status": "success", "message": "Data uploaded successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

# /delete_all (POST)
@limiter.limit("1/hour")
@app.post("/delete_all")
async def delete_all():
    try:
        handler.delete_all()
        return {"status": "success", "message": "All data deleted successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})