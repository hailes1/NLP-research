from config.settings import settings
from dotenv import load_dotenv 
from utils.logger_config import setup_logger
from services.embedding_service import create_embeddings

logger = setup_logger(__name__)

load_dotenv()
client = settings.openai_client

def analytical_retrieval_strategy(query, vector_store, k=4):
    """
    Retrieval strategy for analytical queries focusing on comprehensive coverage.
    
    Args:
        query (str): User query
        vector_store (SimpleVectorStore): Vector store
        k (int): Number of documents to return
        
    Returns:
        List[Dict]: Retrieved documents
    """
    logger.info(f"Executing Analytical retrieval strategy for: '{query}'")
    
    # Define the system prompt to guide the AI in generating sub-questions
    system_prompt = """You are an expert at breaking down complex questions.
    Generate sub-questions that explore different aspects of the main analytical query.
    These sub-questions should cover the breadth of the topic and help retrieve 
    comprehensive information.

    Return a list of exactly 3 sub-questions, one per line.
    """

    # Create the user prompt with the main query
    user_prompt = f"Generate sub-questions for this analytical query: {query}"
    
    # Generate the sub-questions using the LLM
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    # Extract and clean the sub-questions
    sub_queries = response.choices[0].message.content.strip().split('\n')
    sub_queries = [q.strip() for q in sub_queries if q.strip()]
    logger.info(f"Generated sub-queries: {sub_queries}")
    
    # Retrieve documents for each sub-query
    all_results = []
    for sub_query in sub_queries:
        # Create embeddings for the sub-query
        sub_query_embedding = create_embeddings(sub_query)
        # Perform similarity search for the sub-query
        results = vector_store.similarity_search(sub_query_embedding, k=2)
        all_results.extend(results)

    logger.info(f"Retrieved {len(all_results)} results from sub-queries.")

    unique_texts = set()
    diverse_results = []
    
    for result in all_results:
        if result["text"] not in unique_texts:
            unique_texts.add(result["text"])
            diverse_results.append(result)
    
    if len(diverse_results) < k:
        main_query_embedding = create_embeddings(query)
        main_results = vector_store.similarity_search(main_query_embedding, k=k)
        
        for result in main_results:
            if result["text"] not in unique_texts and len(diverse_results) < k:
                unique_texts.add(result["text"])
                diverse_results.append(result)
    
    return diverse_results[:k]