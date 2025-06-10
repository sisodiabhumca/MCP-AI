from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class AIModel(ABC):
    """Abstract base class for AI model implementations"""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the AI model with configuration"""
        pass
    
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text based on the prompt"""
        pass
    
    @abstractmethod
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Generate a response in a chat conversation"""
        pass
    
    @abstractmethod
    def embed_text(self, text: str, **kwargs) -> List[float]:
        """Generate embeddings for the given text"""
        pass
    
    @abstractmethod
    def analyze_image(self, image_data: bytes, prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Analyze an image and generate description or answer questions about it"""
        pass
    
    @abstractmethod
    def moderate_content(self, content: str) -> Dict[str, Any]:
        """Check content for potential violations or inappropriate content"""
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """Return a dictionary of supported capabilities"""
        pass
    
    @property
    @abstractmethod
    def model_info(self) -> Dict[str, Any]:
        """Return information about the model"""
        pass 