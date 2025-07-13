from dotenv import load_dotenv
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document

from services.embedding_service import create_embeddings
from services.document_service import process_document
from utils.logger_config import setup_logger
from utils.generate_response_llm import generate_response
from config.settings import settings

logger = setup_logger(__name__)

load_dotenv()
client = settings.openai_client

def standard_retrieval(pdf_path, test_queries, reference_answers=None):
    """
    standard retrieval on a set of test queries.
    
    This function processes a document, runs standard methods on each test query, and compares their performance. 

    
    Args:
        pdf_path (str): Path to PDF document to be processed as the knowledge source
        test_queries (List[str]): List of test queries to evaluate both retrieval methods
        reference_answers (List[str], optional): Reference answers for evaluation metrics
        
    Returns:
        Dict: Evaluation results containing individual query results and overall comparison
    """
    logger.info("Starting the standard retrieval process")
    chunks, vector_store = process_document(pdf_path)
    
    results = []
    try:
        for i, query in enumerate(test_queries):
            logger.info(f"\n\nQuery {i+1}: {query}")
            
            logger.info("\n--- Standard Retrieval ---")
            query_embedding = create_embeddings(query)
            standard_docs = vector_store.similarity_search(query_embedding, k=4)
            logger.info(f"Standard documents retrieved: {standard_docs}")
            standard_response = generate_response(query, standard_docs, "General")
            
            result = {
                "query": query,
                "standard_retrieval": {
                    "documents": standard_docs,
                    "response": standard_response
                }
            }
            
            if reference_answers and i < len(reference_answers):
                result["reference_answer"] = reference_answers[i]
                
            results.append(result)
            
            logger.info("\n--- Responses ---")
            logger.info(f"Standard: {standard_response[:200]}...")
        
        
        return {
            "results": results,
        }
    except Exception as e:
        logger.error("An error occurred while performing the standard retrieval: %s", e)
        raise e 
    
def hybrid_search(pdf_path, test_queries, reference_answers=None):
    """
    Hybrid search on a set of test queries.
    
    This function processes a document, runs hybrid methods on each test query, and compares their performance. 

    
    Args:
        pdf_path (str): Path to PDF document to be processed as the knowledge source
        test_queries (List[str]): List of test queries to evaluate both retrieval methods
        reference_answers (List[str], optional): Reference answers for evaluation metrics
        
    Returns:
        Dict: Evaluation results containing individual query results and overall comparison
    """
    logger.info("Starting the hybrid search process")
    chunks, vector_store = process_document(pdf_path)
    # initialize the bm25 retriever
    

    results = []
    try:
        for i, query in enumerate(test_queries):
            logger.info(f"\n\nQuery {i+1}: {query}")
            
            logger.info("\n--- Hybrid Search ---")
            docs = [Document(page_content=t, metadata={"source":"source", "chunk":i}) for i,t in enumerate(chunks)]
            bm25_retriever = BM25Retriever.from_documents(docs)
            bm25_retriever.k = 3

            embedding = OpenAIEmbeddings()
            faiss_vectorstore = FAISS.from_documents(docs, embedding)
            # Create a retriever from the vectorstore
            faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 3})

            # initialize the ensemble retriever
            ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever],
                                                weights=[0.5, 0.5])
            
            hybrid_docs = ensemble_retriever.get_relevant_documents(query)

                # Extract page_content from each Document for generating a response
            response_contents = [{"text": doc.page_content} for doc in hybrid_docs]
            hybrid_response = generate_response(query, response_contents, "General")
            
            result = {
                "query": query,
                "hybrid_search": {
                    "documents": hybrid_docs,
                    "response": hybrid_response
                }
            }
            
            if reference_answers and i < len(reference_answers):
                result["reference_answer"] = reference_answers[i]
                
            results.append(result)
            
        return {
            "results": results,
        }
    except Exception as e:
        logger.error("An error occurred while performing the hybrid search: %s", e)
        raise e