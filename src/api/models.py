from pydantic import BaseModel, Field

class Overview(BaseModel):
    question: list = Field(
        default=[
            "What is the main topic of the document?",
            "Can you summarize the key points?",
            "What are the implications of the findings?",
            "How does this relate to current events?",
            "What are the future directions suggested by the document?"
        ],
        description="Default questions to be displayed."
    )
    request_id: str = Field(
        default="",
        description="Unique identifier for the request, used for tracking and logging purposes."
    )
    file_path: str = Field(
        default="",
        description="Path to the PDF file that contains the knowledge source."
    )