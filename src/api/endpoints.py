from fastapi import APIRouter
from api.models import Overview
from research.default_retrieval import standard_retrieval
router = APIRouter()

@router.post("/chat")
def chat(overview: Overview):
    results = standard_retrieval("data/2305.15334v1.pdf", overview.question)
    return {
        "Question": overview.question,
        "results": results,
    }