import fitz
from utils.logger_config import setup_logger

logger = setup_logger(__name__)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file and prints the first `num_chars` characters.

    Args:
    pdf_path (str): Path to the PDF file.

    Returns:
    str: Extracted text from the PDF.
    """
    # Open the PDF file
    try: 
        mypdf = fitz.open(pdf_path)
        all_text = ""  # Initialize an empty string to store the extracted text

        # Iterate through each page in the PDF
        for page_num in range(mypdf.page_count):
            page = mypdf[page_num]  # Get the page
            text = page.get_text("text")  # Extract text from the page
            all_text += text  # Append the extracted text to the all_text string

        return all_text  # Return the extracted text
    except Exception as e:
        logger.error("An error occurred while extracting text from PDF")
        raise e

def chunk_text(text, n, overlap):
    """
    Chunks the given text into segments of n characters with overlap.
    - RESEARCH AREA: What is the best chunking strategy, What are the most recent papers published in this area. 
    
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