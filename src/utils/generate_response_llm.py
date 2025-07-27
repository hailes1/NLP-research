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

def image_summarize(image_url, model="gpt-4-vision-preview"):
    """
    Generate a detailed image summary using a vision-capable OpenAI model.
    
    Args:
        image_url (str): URL to the image to be summarized.
        model (str): Model to use for image analysis.

    Returns:
        str: A detailed summary of the image in various categories, or an error message if unsuccessful.
    """
    try:
        # Initialize the chat interface with a vision-capable model
        chat = ChatOpenAI(model=model, max_tokens=1024)

        # Define system and user prompts
        system_prompt = """You are a vision-capable assistant. Analyze the image and provide a detailed summary
                          in the following categories. If any category is not applicable, state 'No information available'. """

        user_prompt = f"""
        Please provide bullet point summaries for the image in the following categories:
        - Medium: 
        - Subject: 
        - Scene: 
        - Style: 
        - Artistic Influence or Movement: 
        - Website: 
        - Color: 
        - Lighting:
        - Additional Details: 

        Image URL: {image_url}
        """

        # Execute the analysis
        response = chat.invoke(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        return response.content

    except Exception as e:
        logger.error("Failed to generate image summary: %s", str(e))
        return "Error: Unable to generate a summary for the image."