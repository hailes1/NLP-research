import requests
import os
import re
from datetime import datetime
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


        guardian_web_urls = [result["webUrl"] for result in data["response"]["results"] if "webUrl" in result]
        guardian_web_titles = [result["webTitle"] for result in data["response"]["results"] if "webTitle" in result]
        guardian_news_updates = save_news_data(guardian_web_urls, guardian_web_titles)


        return guardian_news_updates
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
    logger.info(f"Fetch NYT Data: {response}")
    if response.status_code == 200:
        data = response.json()

        nyt_web_urls = [result["url"] for result in data["results"] if "url" in result]
        nyt_web_titles = [result["title"] for result in data["results"] if "title" in result]
        nyt_news_updates = save_news_data(nyt_web_urls, nyt_web_titles)


        logger.info("Successfully fetched data from NYT API.")
        return nyt_web_titles
    else:
        logger.info(f"Error: {response.status_code}, {response.text}")
        return None
    

def save_news_data(web_urls, web_titles):
    """
    Saves news articles from a list of URLs to individual Markdown files in a specified directory.
    
    Args:
        web_urls (list): The list containing the URLs of the news articles.
        guardian_web_titles (list): The list containing the titles of the news articles.
    """
    logger.info("Starting the process of saving news data.")

    output_folder = "./data/todays_news"
    os.makedirs(output_folder, exist_ok=True)
    logger.info("Output directory '%s' is ready.", output_folder)
    
    content = []
    for index, (web_url, title) in enumerate(zip(web_urls, web_titles)):
        logger.info("Processing URL %s with title '%s'", web_url, title)
        try:
            markdown_content = process_html_to_markdown(web_url)  # Fetch the article content in Markdown format
            markdown_content = re.sub(r'http[s]?://\S+', '', markdown_content)
            content.append({
                "document_id": index,
                "title": title,
                "content": markdown_content
            })

            # Define the file path using the index as the document ID
            md_file_path = os.path.join(output_folder, f"article_{index}.md")
            
            # Save the Markdown content along with the title to the file
            with open(md_file_path, "w", encoding="utf-8") as md_file:
                md_file.write(f"# {title}\n\n")
                md_file.write(markdown_content)
            
            logger.info("Successfully saved article to %s", md_file_path)

        except Exception as e:
            logger.error("Failed to process and save URL %s: %s", web_url, str(e))

    logger.info("Completed saving all articles.")
    return content