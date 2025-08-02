import fitz
import requests
from bs4 import BeautifulSoup
import html2text
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
    
def process_html_to_markdown(URL):
    """
    Converts the content of a webpage at the specified URL into plain text format.

    Args:
        URL (str): The URL of the webpage to be converted.

    Returns:
        str: The plain text content of the webpage, including the title
             and main body content if identified, or an error message if extraction fails.
    """
    try:
        # Fetch the HTML content
        response = requests.get(URL)
        logger.info(f'logger.info(f"Fetching HTML content from URL:{response}")')
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the title
        title = soup.find("title").get_text()

        # Extract the main article content
        article_body = soup.find("div", {"class": "article-body-commercial-selector"})
        if article_body:
            # Convert the HTML content to Markdown
            markdown_converter = html2text.HTML2Text()
            markdown_converter.ignore_links = False  # Keep links in the Markdown
            markdown_content = markdown_converter.handle(str(article_body))

            # Remove newlines and extra spaces from the Markdown content
            plain_text_content = " ".join(markdown_content.split())

            return f"{title} - {plain_text_content}"
        else:
            return "Could not find the article body in the HTML."
    except requests.RequestException as e:
        logger.error("An error occurred while fetching the URL: %s", str(e))
        return f"Failed to fetch the URL. Error: {str(e)}"
