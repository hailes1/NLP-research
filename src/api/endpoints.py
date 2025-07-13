from fastapi import APIRouter, HTTPException, File, UploadFile
from api.models import Overview
import os

from utils.logger_config import setup_logger
from research.default_retrieval import standard_retrieval
from utils.generate_request_id import RequestIDGenerator

logger = setup_logger(__name__)

router = APIRouter()

@router.post("/upload_file")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise logger.error(status_code=400, detail="The file provided doesn't meet the required format. Only PDF files are allowed.")

    file_path = f"data/{file.filename}"
    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.info(f"File saved to {file_path}")
    except Exception as e:
        raise logger.error(status_code=500, detail=f"Error saving file: {e}")

    logger.info(f"File {file.filename} uploaded successfully with content type {file.content_type}")
    request_id = RequestIDGenerator.generate_request_id()

    return {"request_id": request_id, "file_path": file_path}

@router.post("/chat/similarity_search")
def chat(overview: Overview):
    results = standard_retrieval(overview.file_path, overview.question)
    simplified_results = [
        {
            "query": result["query"],
            "response": result["standard_retrieval"]["response"]
        }
        for result in results["results"] 
    ]
    
    return {
        "Question": overview.question,
        "results": simplified_results,
    }