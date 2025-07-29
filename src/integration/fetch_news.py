import requests
import os
from dotenv import load_dotenv
from services.data_utils import process_html_to_markdown
from utils.logger_config import setup_logger

load_dotenv()
logger = setup_logger(__name__)

def fetch_guardian_data(query):
    """
    Fetch data from the Guardian API based on a query and save it to a JSON file.

    Args:
        query (str): The search query for the Guardian API.

    Returns:
        dict: The JSON response from the Guardian API if successful, None otherwise.
    """
    GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
    url = f"http://content.guardianapis.com/search?q={query}&api-key={GUARDIAN_API_KEY}"

    logger.info("Fetching data from Guardian API with query: %s", query)
    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        logger.info("Successfully fetched data from Guardian API.")
        return data
    else:
        logger.info(f"Error: {response.status_code}, {response.text}")
        return None
    
def fetch_nyt_data(section):
    """
    Fetch data from the NYT API based on a query and save it to a JSON file. 

    Args: 
        query (str): The search query for the NYT API.
    
    Returns: 
        dict: The JSON response from the NYT API if successful, None otherwise. 

    """
    NYT_API_KEY = os.getenv("NYT_API_KEY")
    url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={NYT_API_KEY}"

    logger.info("Fetching data from NYT API with section: %s", section)

    response = requests.get(url)

    if response.status_code == 200:
        response_data = response.json()
        logger.info("Successfully fetched data from NYT API.")
        return response_data
    else:
        logger.info(f"Error: {response.status_code}, {response.text}")
        return None
    
def save_news_data(data):
    """
    Saves news articles from a list of URLs to individual Markdown files in a specified directory.

    This function will iterate over a list of URLs, convert each webpage's content to Markdown format
    using the `process_html_to_markdown` function, and save the content into a uniquely named Markdown file.
    
    Args:
        web_urls (List[str]): A list of URLs pointing to the news articles to be saved.
    """
    logger.info("Starting the process of saving news data.")

    web_urls = [result["webUrl"] for result in data["response"]["results"] if "webUrl" in result]
    # Create the folder if it doesn't exist
    output_folder = "./data/todays_news"
    os.makedirs(output_folder, exist_ok=True)
    logger.info("Output directory '%s' is ready.", output_folder)
    
    content = []
    # Iterate through the URLs and save the Markdown content
    for index, web_url in enumerate(web_urls):
        logger.info("Processing URL %s", web_url)
        try:
            markdown_content = process_html_to_markdown(web_url)  # Fetch the article content in Markdown format

            # Define the file path using the index as the document ID
            file_path = os.path.join(output_folder, f"{index}.md")
            
            # Save the Markdown content to the file
            with open(file_path, "w") as md_file:
                md_file.write(markdown_content)
            
            content.append({
                "document_id": index,
                "content": markdown_content
            })
            logger.info("Successfully saved article to %s", file_path)
        except Exception as e:
            logger.error("Failed to process and save URL %s: %s", web_url, str(e))
    logger.info("Completed saving all articles.")
    return content
