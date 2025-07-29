from fastapi import APIRouter, HTTPException, File, UploadFile
from api.models import Overview, NewsQuery
import os

from utils.logger_config import setup_logger
from research.default_retrieval import standard_retrieval, hybrid_search
from integration.fetch_news import fetch_guardian_data, fetch_nyt_data, save_news_data
from utils.generate_request_id import RequestIDGenerator

logger = setup_logger(__name__)

router = APIRouter()

@router.post("/upload_file", tags=["Upload"])
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF file for processing.

    This endpoint allows users to upload a PDF file that will be saved to the server
    for further analysis. The function checks the file type to ensure it is a PDF
    and saves the file to a designated directory, generating a unique request ID
    for reference.
    """
    if file.content_type != "application/pdf":
        raise logger.error(status_code=400, 
                           detail="The file provided doesn't meet the required format. Only PDF files are allowed.")

    file_path = f"data/{file.filename}"
    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        logger.info(f"File saved to {file_path}")
    except Exception as e:
        raise logger.error(status_code=500, 
                           detail=f"Error saving file: {e}")

    logger.info(f"File {file.filename} uploaded successfully with content type {file.content_type}")
    request_id = RequestIDGenerator.generate_request_id()

    return {"request_id": request_id, "file_path": file_path}


@router.post("/chat", tags=["Rag Research"])
def chat(overview: Overview):
    """
    Perform similarity search on an uploaded PDF.

    Utilizes standard retrieval and hybrid retrieval methods to find content in the PDF that is similar
    to the user's question, returning concise responses for easy evaluation.
    """
    if (overview.search_type == 'standard'):
        results = standard_retrieval(overview.file_path, overview.question)
        simplified_results = [
            {
                "query": result["query"],
                "response": result["standard_retrieval"]["response"]
            }
            for result in results["results"]
        ]
    else: 
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
def summarize_recent_news(newsquery: NewsQuery):
    """
    Fetch and summarize recent news articles.

    Retrieves news articles based on a query from the Guardian API and summarizes
    the content for quick updates. Provides a request ID for tracking these summaries.

    """
    logger.info("Fetching and summarizing news with query: '%s'", newsquery.query)
    request_id = RequestIDGenerator.generate_request_id()
    guardian_data = fetch_guardian_data(newsquery.query)
    nyt_data = fetch_nyt_data(newsquery.query)
    news_updates = save_news_data(guardian_data)
    return {"guardian_news_updates": news_updates, 
            "nyt_news_updates": nyt_data,
            "requestID": request_id}
