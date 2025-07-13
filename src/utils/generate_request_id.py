import uuid
from utils.logger_config import setup_logger

logger = setup_logger(__name__)

class RequestIDGenerator:
    """
    A utility class to generate unique request IDs.
    """
    
    @staticmethod
    def generate_request_id():
        """
        Generate a unique request ID using UUID.
        
        Returns:
            str: A unique request ID.
        """
        request_id = str(uuid.uuid4())
        logger.info(f"Generated new request ID: {request_id}")
        return request_id
