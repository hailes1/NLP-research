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
    search_type: str = Field(
        default="standard",
        description="Type of search to perform. Options include 'standard' for basic retrieval and 'hybrid' for BM25 vector search."
    )
    chunking_strategy: str = Field(
        default="fixed",
        description="Strategy used for chunking the document. Options include 'fixed', 'semantic or structure_based"
    )
    request_id: str = Field(
        default="",
        description="Unique identifier for the request, used for tracking and logging purposes."
    )
    file_path: str = Field(
        default="",
        description="Path to the file that contains the knowledge source."
    )

class NewsQuery(BaseModel):
    query: str = Field(
        default="",
        description="Search query for fetching news articles."
    )
class ImageQuery(BaseModel):
    question: str = Field(
        default="What is the main topic of the document?",
        description="Search query for fetching news articles."
    )
    request_id: str = Field(
        default="",
        description="Unique identifier for the request, used for tracking and logging purposes."
    )
    file_path: str = Field(
        default="",
        description="Path to the file that contains the knowledge source."
    )
    model: str = Field(
        default="pixtral-12b-2409",
        description="Model to be used for image summarization."
    )