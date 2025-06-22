from pydantic import BaseModel, Field

class Overview(BaseModel):
    question: list = Field(
        default=[
            "What are the talking points I can generate from the FACILITATING LARGE LANGUAGE MODELS TO MASTER 16000+ REAL-WORLD APIS paper?",
            "What are some the most recent developments on AI?"
        ],
        description="Default questions to be displayed."
    )