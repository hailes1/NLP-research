import numpy as np
from dotenv import load_dotenv
from utils.logger_config import setup_logger

logger = setup_logger(__name__)
load_dotenv()


class SimpleVectorStore:
    """
    A simple vector store implementation using NumPy.
    """
    def __init__(self):
        """
        Initialize the vector store.
        """
        self.vectors = []  # List to store embedding vectors
        self.texts = []  # List to store original texts
        self.metadata = []  # List to store metadata for each text
        logger.info("Initialized SimpleVectorStore with empty vectors, texts, and metadata.")

    def add_item(self, text, embedding, metadata=None):
        """
        Add an item to the vector store.

        Args:
        text (str): The original text.
        embedding (List[float]): The embedding vector.
        metadata (dict, optional): Additional metadata.
        """
        self.vectors.append(np.array(embedding))  # Convert embedding to numpy array and add to vectors list
        self.texts.append(text)  # Add the original text to texts list
        self.metadata.append(metadata or {})  # Add metadata to metadata list, default to empty dict if None
        #logger.info(f"Added item to vector store - embedding_length={len(embedding)}, metadata={metadata}.")

    def similarity_search(self, query_embedding, k=5, filter_func=None):
        """
        Find the most similar items to a query embedding.

        Args:
        query_embedding (List[float]): Query embedding vector.
        k (int): Number of results to return.
        filter_func (callable, optional): Function to filter results.

        Returns:
        List[Dict]: Top k most similar items with their texts and metadata.
        """
        if not self.vectors:
            logger.info("Similarity search called, but vector store is empty.")
            return []

        logger.info(f"Performing similarity search with query_embedding of length {len(query_embedding)} and k={k}.")
        
        query_vector = np.array(query_embedding)
        
        similarities = []
        for i, vector in enumerate(self.vectors):
            # Apply filter if provided
            if filter_func and not filter_func(self.metadata[i]):
                #logger.info(f"Item at index {i} filtered out by filter_func.")
                continue
                
            # Calculate cosine similarity
            similarity = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            similarities.append((i, similarity)) 
            #logger.info(f"Calculated similarity for index {i}: {similarity:.4f}")

        similarities.sort(key=lambda x: x[1], reverse=True)
        logger.info(f"Sorted similarities: {similarities[:k]}")

        results = []
        for i in range(min(k, len(similarities))):
            idx, score = similarities[i]
            results.append({
                "text": self.texts[idx],
                "metadata": self.metadata[idx], 
                "similarity": score 
            })
            #logger.info(f"Top result {i + 1}: text='{self.texts[idx][:30]}...', similarity={score:.4f}, metadata={self.metadata[idx]}")

        logger.info(f"Returning top {len(results)} results from similarity search.")
        return results 