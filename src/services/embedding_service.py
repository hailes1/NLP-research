from dotenv import load_dotenv 
from utils.logger_config import setup_logger
from config.settings import settings
logger = setup_logger(__name__)

load_dotenv()
client = settings.openai_client


def create_embeddings(text, model="text-embedding-3-small"):

    """
    RESEARCH AREA: What is the best embedding model? What are the differences is there any papers that are most recently published/most cited that 
    cover this area. 
    - Take a look at this paper: https://arxiv.org/html/2406.01607v2


    Creates embeddings for the given text.

    Args:
    text (str or List[str]): The input text(s) for which embeddings are to be created.
    model (str): The model to be used for creating embeddings.

    Returns:
    List[float] or List[List[float]]: The embedding vector(s).
    """

    logger.info("Creating embeddings for text with model: %s", model)
    try:
        # Handle both string and list inputs by converting string input to a list
        input_text = text if isinstance(text, list) else [text]
        
        # Create embeddings for the input text using the specified model
        response = client.embeddings.create(
            model=model,
            input=input_text
        )
        
        # If the input was a single string, return just the first embedding
        if isinstance(text, str):
            return response.data[0].embedding
        
        # Otherwise, return all embeddings for the list of texts
        logger.info("The embeddings where successfully created")
        return [item.embedding for item in response.data]
    except Exception as e:
        logger.error("An error occurred while creating embeddings: %s", e)
        raise e