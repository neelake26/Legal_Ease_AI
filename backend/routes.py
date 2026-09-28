from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str
    language: str
    details: str


class DocumentResponse(BaseModel):
    generated_document: str


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()
        result = generator.generate_document(
            document_type=request.document_type,
            language=request.language,
            details=request.details,
        )
        return {"generated_document": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))