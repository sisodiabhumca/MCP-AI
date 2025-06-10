from typing import Dict, Any, List, Optional
import google.generativeai as genai
from PIL import Image
import io

from ...core.ai_interface import AIModel

class GeminiAdapter(AIModel):
    """Google Gemini implementation of the AI model interface"""
    
    def __init__(self):
        self.model = None
        self.vision_model = None
        self.embedding_model = None
        self._capabilities = {
            "text_generation": True,
            "chat": True,
            "embeddings": True,
            "image_analysis": True,
            "moderation": False,
            "image_generation": False
        }
        
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the Gemini client with configuration"""
        api_key = config.get('api_key')
        genai.configure(api_key=api_key)
        
        # Initialize models
        model_name = config.get('model', 'gemini-pro')
        self.model = genai.GenerativeModel(model_name)
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')
        self.embedding_model = genai.GenerativeModel('embedding-001')
        
    def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text using Gemini"""
        try:
            response = self.model.generate_content(prompt, **kwargs)
            
            return {
                "text": response.text,
                "usage": {},  # Gemini doesn't provide usage stats
                "model": "gemini-pro"
            }
        except Exception as e:
            return {"error": str(e)}
            
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Generate a chat response using Gemini"""
        try:
            # Convert messages to Gemini format
            chat = self.model.start_chat()
            
            # Process all messages except the last one
            for message in messages[:-1]:
                if message["role"] == "user":
                    chat.send_message(message["content"])
                # Note: Gemini handles assistant responses automatically
            
            # Process the last message and get response
            last_message = messages[-1]
            response = chat.send_message(last_message["content"])
            
            return {
                "response": response.text,
                "usage": {},  # Gemini doesn't provide usage stats
                "model": "gemini-pro"
            }
        except Exception as e:
            return {"error": str(e)}
            
    def embed_text(self, text: str, **kwargs) -> List[float]:
        """Generate embeddings using Gemini"""
        try:
            response = self.embedding_model.embed_content(text)
            return response.embedding
        except Exception as e:
            return []
            
    def analyze_image(self, image_data: bytes, prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Analyze an image using Gemini Vision"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Generate response
            response = self.vision_model.generate_content(
                [prompt or "What's in this image?", image],
                **kwargs
            )
            
            return {
                "description": response.text,
                "model": "gemini-pro-vision"
            }
        except Exception as e:
            return {"error": str(e)}
            
    def moderate_content(self, content: str) -> Dict[str, Any]:
        """Content moderation (not directly supported by Gemini)"""
        return {
            "error": "Content moderation is not supported by Gemini",
            "flagged": False,
            "categories": {},
            "scores": {}
        }
        
    @property
    def capabilities(self) -> Dict[str, bool]:
        """Return Gemini's capabilities"""
        return self._capabilities
        
    @property
    def model_info(self) -> Dict[str, Any]:
        """Return information about the Gemini model"""
        return {
            "provider": "Google",
            "model": "gemini-pro",
            "type": "Large Language Model",
            "capabilities": self.capabilities
        } 