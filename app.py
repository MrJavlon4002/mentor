from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from document_hendler import DocumentHandler

app = FastAPI()
handler = DocumentHandler()

# -----------------------------
# Data Uploading Endpoint
# -----------------------------

class DataTakingRequest(BaseModel):
    text: str
    project: str
    languages: List[str]

@app.post("/data_taking")
async def data_taking(request: DataTakingRequest):
    try:
        handler.data_upload(
            project=request.project,
            text=request.text,
            languages=request.languages
        )
        return {"status": "success", "message": "Data inserted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Question Asking Endpoint
# -----------------------------

class AskQuestionRequest(BaseModel):
    project_name: str
    user_input: str
    history: Optional[List[str]] = []
    lang: str

@app.post("/ask_question")
async def ask_question(request: AskQuestionRequest):
    try:
        answer = handler.ask_question(
            history=request.history,
            user_input=request.user_input,
            project_name=request.project_name,
            lang=request.lang
        )
        return {"status": "success", "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
