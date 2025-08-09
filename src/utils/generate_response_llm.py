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