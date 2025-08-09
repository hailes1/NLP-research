import base64
import requests
import os
from mistralai import Mistral


from utils.logger_config import setup_logger

logger = setup_logger(__name__)

def image_summarize(file_path, question, model = "pixtral-12b-2409"):
    """
    Summarize the content of an image using Mistral's Pixtral model.
    
    Args:
        file_path (str): Path to the image file.
        question (str): Question to ask about the image.
        
    Returns:
        str: Summary of the image content.
    """
    try:
        logger.info(f"Opening image file from path: {file_path}")
        with open(file_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{base64_image}"
            logger.info("Image file successfully encoded to base64.")
    except FileNotFoundError:
        logger.error("Error: The specified image file was not found.")
        return "Error: The specified image file was not found."
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {e}"

    # Retrieve the API key from environment variables
    try:
        api_key = os.environ["MISTRAL_API_KEY"]
        logger.info("API key successfully retrieved from environment variables.")
    except KeyError:
        logger.error("Error: MISTRAL_API_KEY environment variable not set.")
        return "Error: MISTRAL_API_KEY environment variable not set."

    # Initialize the Mistral client
    client = Mistral(api_key=api_key)
    logger.info("Mistral client initialized.")

    # Define the messages for the chat
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question
                },
                {
                    "type": "image_url",
                    "image_url": image_url
                }
            ]
        }
    ]
    logger.info(f"Messages prepared for the chat: {messages}")

    # Get the chat response
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=messages
        )
        logger.info("Chat response received successfully.")
    except Exception as e:
        logger.error(f"Error while getting chat response: {e}")
        return f"Error: {e}"

    return chat_response.choices[0].message.content