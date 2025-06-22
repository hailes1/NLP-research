from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from services.document_service import process_document
from api.endpoints import router

load_dotenv() 
app = FastAPI(title="Retrieval Augument Generation: Document Retrieval", version="1.0.0")
app.include_router(router)