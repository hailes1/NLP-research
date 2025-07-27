from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from services.document_service import process_document
from api.endpoints import router

load_dotenv() 
app = FastAPI(title="RAG Framework: Enhanced Document Understanding", version="1.0.0")
app.include_router(router)