from services.data_utils import extract_text_from_pdf, chunk_text
from services.embedding_service import create_embeddings
from services.vector_store import SimpleVectorStore
from utils.logger_config import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)

def process_document(pdf_path, chunk_size=1000, chunk_overlap=200):
    """
    Process a document for use with adaptive retrieval.

    Args:
    pdf_path (str): Path to the PDF file.
    chunk_size (int): Size of each chunk in characters.
    chunk_overlap (int): Overlap between chunks in characters.

    Returns:
    Tuple[List[str], SimpleVectorStore]: Document chunks and vector store.
    """
    # Extract text from the PDF file
    logger.info("Extracting text from PDF...")
    extracted_text = extract_text_from_pdf(pdf_path)

    # Chunk the extracted text
    logger.info("Chunking text...")
    chunks = chunk_text(extracted_text, chunk_size, chunk_overlap)
    logger.info(f"Created {len(chunks)} text chunks")
    
    # Create embeddings for the text chunks
    logger.info("Creating embeddings for chunks...")
    chunk_embeddings = create_embeddings(chunks)
    
    # Initialize the vector store
    store = SimpleVectorStore()
    
    # Add each chunk and its embedding to the vector store with metadata
    for i, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings)):
        store.add_item(
            text=chunk,
            embedding=embedding,
            metadata={"index": i, "source": pdf_path}
        )
    
    logger.info(f"Added {len(chunks)} chunks to the vector store")
    # Return the chunks and the vector store
    return chunks, store