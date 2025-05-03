from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
from document_hendler import DocumentHandler

ALLOWED_IPS = {"127.0.0.1", "192.168.1.10", "172.19.0.1"}

class IPWhitelistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        print(f"Client IP: {client_ip}")
        if client_ip not in ALLOWED_IPS:
            return JSONResponse(
                status_code=403,
                content={"detail": "Forbidden: IP not allowed"}
            )
        return await call_next(request)

app = FastAPI()
app.add_middleware(IPWhitelistMiddleware)

handler = DocumentHandler()

# -----------------------------
# Pydantic Models
# -----------------------------

class ProductCreateRequest(BaseModel):
    details: Dict
    project_name: str
    lang: str

class ProductGetRequest(BaseModel):
    project_name: str
    product_id: str
    languages: List[str]

class ProductUpdateRequest(BaseModel):
    project_name: str
    product_id: str
    details: Dict

class ProductDeleteRequest(BaseModel):
    project_name: str
    product_id: str
    languages: List[str]

class AskQuestionRequest(BaseModel):
    project_name: str
    user_question: str
    history: Optional[List[str]] = []
    lang: str
    company_data: Optional[Dict] = {}

class DataTakingRequest(BaseModel):
    text: str
    project: str
    languages: List[str]

# -----------------------------
# Endpoints
# -----------------------------

@app.post("/products")
async def create_product(request: ProductCreateRequest):
    try:
        handler.create_product(
            details=request.details,
            project_name=request.project_name,
            lang=request.lang
        )
        return {"status": "success", "message": f"Product created for project '{request.project_name}'."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.get("/products/{product_id}")
async def get_product(request: ProductGetRequest):
    try:
        product = handler.get_product(
            project_name=request.project_name,
            product_id=request.product_id,
            languages=request.languages
        )
        if product == "Product not found in any language.":
            return JSONResponse(status_code=404, content={"detail": product})
        return {"status": "success", "product": product}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.get("/products")
async def get_all_products(project_name: str, languages: List[str]):
    try:
        products = handler.get_all_products(
            project_name=project_name,
            languages=languages
        )
        if products == "No products found in any language.":
            return JSONResponse(status_code=404, content={"detail": products})
        return {"status": "success", "products": products}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.put("/products/{product_id}")
async def update_product(request: ProductUpdateRequest):
    try:
        handler.update_product(
            project_name=request.project_name,
            product_id=request.product_id,
            details=request.details
        )
        return {"status": "success", "message": f"Product '{request.product_id}' updated."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.delete("/products/{product_id}")
async def delete_product(request: ProductDeleteRequest):
    try:
        success = handler.delete_product(
            project_name=request.project_name,
            product_id=request.product_id,
            languages=request.languages
        )
        if success:
            return {"status": "success", "message": f"Product '{request.product_id}' deleted."}
        return JSONResponse(status_code=400, content={"detail": "Failed to delete product."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/ask_question")
async def ask_question(request: AskQuestionRequest):
    try:
        question_details = {
            "history": request.history,
            "user_question": request.user_question,
            "project_name": request.project_name,
            "lang": request.lang,
            "company_data": request.company_data
        }
        answer = handler.ask_question(question_details=question_details)
        return {"status": "success", "answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/data_taking")
async def data_taking(request: DataTakingRequest):
    try:
        handler.data_upload(
            project_name=request.project,
            row_data=request.text,
            languages=request.languages
        )
        return {"status": "success", "message": "Data inserted successfully."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
