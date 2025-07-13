import os
from dotenv import load_dotenv
from openai import OpenAI  # Assuming OpenAI is the correct library you're using

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI client
    @property
    def openai_client(self):
        return OpenAI(
            base_url="https://api.openai.com/v1/",
            api_key=self.OPENAI_API_KEY
        )

# Create a global settings instance
settings = Settings()