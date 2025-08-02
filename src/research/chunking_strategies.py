import re
from collections import Counter
import math

from utils.logger_config import setup_logger

logger = setup_logger(__name__)

def fixed_size_chunking(text, n, overlap):
    """
    Chunks the given text into segments of n characters with overlap. 
    
    Args:
    text (str): The text to be chunked.
    n (int): The number of characters in each chunk.
    overlap (int): The number of overlapping characters between chunks.

    Returns:
    List[str]: A list of text chunks.
    """
    logger.info(f"Chunking text into segments of length {n} with proper chunking and overlap")
    try:
        chunks = []  # Initialize an empty list to store the chunks
        
        # Loop through the text with a step size of (n - overlap)
        for i in range(0, len(text), n - overlap):
            # Append a chunk of text from index i to i + n to the chunks list
            chunks.append(text[i:i + n])
        return chunks  # Return the list of text chunks
    except Exception as e:
        logger.error("An error occurred while chunking the text: %s", e)
        raise e

def cosine_similarity(vec1, vec2):
    """
    Computes the cosine similarity between two vectors represented as dictionaries.
    
    Args:
    vec1 (dict): A dictionary representing the first vector where keys are elements and values are frequencies.
    vec2 (dict): A dictionary representing the second vector.

    Returns:
    float: The cosine similarity between the two vectors.
    """
    logger.info("Calculating cosine similarity between two vectors")
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        logger.warning("Denominator is zero. Returning similarity as 0.0")
        return 0.0
    
    similarity = float(numerator) / denominator
    logger.info(f"Cosine similarity calculated: {similarity}")
    return similarity


def create_embedding(text):
    """
    Creates a word frequency embedding from a given text.
    
    Args:
    text (str): The text to create an embedding from.

    Returns:
    Counter: A Counter object representing word frequencies.
    """
    logger.info("Creating embedding from text")
    words = re.findall(r'\w+', text.lower())
    embedding = Counter(words)
    logger.info(f"Embedding created with {len(embedding)} unique words")
    return embedding


def semantic_chunking(text, similarity_threshold=0.5):
    """
    Divides text into chunks based on semantic similarity between sentences.
    
    Args:
    text (str): The complete text to chunk.
    similarity_threshold (float): The threshold for cosine similarity to decide chunk continuation.

    Returns:
    List[str]: A list of semantically meaningful text chunks.
    """
    logger.info("Starting semantic chunking of text")
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = sentences[0]
    current_embedding = create_embedding(current_chunk)
    
    for sentence in sentences[1:]:
        sentence_embedding = create_embedding(sentence)
        similarity = cosine_similarity(current_embedding, sentence_embedding)
        
        if similarity >= similarity_threshold:
            current_chunk += " " + sentence
            current_embedding = create_embedding(current_chunk)
            logger.debug("Appending sentence to current chunk due to high similarity")
        else:
            chunks.append(current_chunk)
            logger.info("Chunk finalized and added to list")
            current_chunk = sentence
            current_embedding = sentence_embedding
    
    chunks.append(current_chunk)
    logger.info("Final chunk added to list")
    return chunks


def structure_based_chunking(text):
    """
    Chunks text based on structural elements like headings and paragraphs.
    
    Args:
    text (str): The text to be chunked based on structure.

    Returns:
    List[str]: A list of text chunks defined by structural elements.
    """
    logger.info("Starting structure-based chunking of text")
    patterns = {
        'heading': r'^#+\s+.*$',
        'paragraph': r'^(?!#+\s+).*(?:\n(?!#+\s+).+)*',
    }
    
    chunks = []
    lines = text.split('\n')
    current_chunk = ''
    
    for line in lines:
        if re.match(patterns['heading'], line):
            if current_chunk:
                chunks.append(current_chunk.strip())
                logger.info("Chunk finalized and added to list based on heading")
            current_chunk = line + '\n'
        elif re.match(patterns['paragraph'], line):
            current_chunk += line + '\n'
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                logger.info("Chunk finalized and added to list based on paragraph")
            current_chunk = ''
    
    if current_chunk:
        chunks.append(current_chunk.strip())
        logger.info("Final chunk added to list")

    return chunks

