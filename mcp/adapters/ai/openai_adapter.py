from typing import Dict, Any, List, Optional
import openai
from openai import OpenAI
import base64

from ...core.ai_interface import AIModel

class OpenAIAdapter(AIModel):
    """OpenAI implementation of the AI model interface"""
    
    def __init__(self):
        self.client = None
        self.model = "gpt-4"
        self.image_model = "dall-e-3"
        self._capabilities = {
            "text_generation": True,
            "chat": True,
            "embeddings": True,
            "image_analysis": True,
            "moderation": True,
            "image_generation": True
        }
        
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the OpenAI client with configuration"""
        api_key = config.get('api_key')
        self.model = config.get('model', self.model)
        # The OpenAI v1.x client does not accept api_key in the constructor
        # It should be set via environment variable or passed per-request
        self.client = OpenAI()
        
    def generate_text(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate text using OpenAI's completion API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            
            return {
                "text": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else {},
                "model": response.model
            }
        except Exception as e:
            return {"error": str(e)}
            
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Generate a response in a chat conversation using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            
            return {
                "response": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else {},
                "model": response.model
            }
        except Exception as e:
            return {"error": str(e)}
            
    def embed_text(self, text: str, **kwargs) -> List[float]:
        """Generate embeddings using OpenAI's embedding API"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text,
                **kwargs
            )
            return response.data[0].embedding
        except Exception as e:
            return []
            
    def analyze_image(self, image_data: bytes, prompt: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Analyze an image using OpenAI's GPT-4 Vision API"""
        try:
            # Convert image bytes to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt or "What's in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=300,
                **kwargs
            )
            
            return {
                "description": response.choices[0].message.content,
                "model": response.model
            }
        except Exception as e:
            return {"error": str(e)}
            
    def moderate_content(self, content: str) -> Dict[str, Any]:
        """Check content using OpenAI's moderation API"""
        try:
            response = self.client.moderations.create(input=content)
            return response.results[0].dict()
        except Exception as e:
            return {"error": str(e)}
            
    @property
    def capabilities(self) -> Dict[str, bool]:
        """Return OpenAI's capabilities"""
        return self._capabilities
        
    @property
    def model_info(self) -> Dict[str, Any]:
        """Return information about the OpenAI model"""
        return {
            "provider": "OpenAI",
            "model": self.model,
            "image_model": self.image_model,
            "type": "Large Language Model",
            "capabilities": self.capabilities
        } 