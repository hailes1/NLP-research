from services.embedding_service import create_embeddings
from services.document_service import process_document
from dotenv import load_dotenv
from utils.logger_config import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

load_dotenv()
client = settings.openai_client

def generate_response(query, results, query_type, model="gpt-3.5-turbo"):
    """
    Generate a response based on query, retrieved documents, and query type.
    
    Args:
        query (str): User query
        results (List[Dict]): Retrieved documents
        query_type (str): Type of query
        model (str): LLM model
        
    Returns:
        str: Generated response
    """
    context = "\n\n---\n\n".join([r["text"] for r in results])
    system_prompt = """You are a helpful assistant. Answer the question based on the provided context. If you cannot answer from the context, acknowledge the limitations."""
    
    user_prompt = f"""
    Context:
    {context}

    Question: {query}

    Please provide a helpful response based on the context.
    """
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.content

def standard_retrieval(pdf_path, test_queries, reference_answers=None):
    """
    Compare adaptive retrieval with standard retrieval on a set of test queries.
    
    This function processes a document, runs both standard and adaptive retrieval methods
    on each test query, and compares their performance. If reference answers are provided,
    it also evaluates the quality of responses against these references.
    
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