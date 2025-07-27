from fastapi import APIRouter, HTTPException, File, UploadFile
from api.models import Overview, NewsQuery
import os

from utils.logger_config import setup_logger
from research.default_retrieval import standard_retrieval, hybrid_search
from integration.fetch_news import fetch_guardian_data, save_news_data
from utils.generate_request_id import RequestIDGenerator

logger = setup_logger(__name__)

router = APIRouter()

@router.post("/upload_file", tags=["File-Upload"])
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF file for further processing.
    """
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


@router.post("/chat/similarity_search", tags=["Rag-Search"])
def chat(overview: Overview):
    """
    Endpoint to perform similarity search on the uploaded PDF.
    """
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


@router.post("/chat/hybrid_search", tags=["Rag-Search"])
def chat(overview: Overview):
    """
    Endpoint to perform hybrid search on the uploaded PDF.
    """
    results = hybrid_search(overview.file_path, overview.question)
    logger.info(results)
    simplified_results = [
        {
            "query": result["query"],
            "response": result["hybrid_search"]["response"]
        }
        for result in results["results"] 
    ]
     
    return {
        "Question": overview.question,
        "results": simplified_results,
    }


@router.post("/news/recent", tags=["News"])
def fetch_recent_news(newsquery: NewsQuery):
    """
    Endpoint to fetch recent news and generate a small news update.
    """
    # Logic to fetch recent news and generate updates
    request_id = RequestIDGenerator.generate_request_id()
    data = fetch_guardian_data(newsquery.query)
    news_updates = save_news_data(data)
    return {"news_updates": news_updates, 
            "requestID": request_id}