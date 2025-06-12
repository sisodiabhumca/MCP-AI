from typing import Dict, List, Optional, Any
from mcp.core.ai_interface import AIModel
import anthropic

class ClaudeAdapter(AIModel):
    """Adapter for Anthropic's Claude models."""
    
    def __init__(self):
        self.client = None
        self._capabilities = {
            "text_generation": True,
            "chat": True,
            "embeddings": False,  # Claude doesn't have native embedding support yet
            "image_analysis": True,  # Claude 3 supports image analysis
            "moderation": True
        }
        self.default_model = "claude-3-opus-20240229"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the Claude client."""
        self.api_key = config.get('api_key')
        self.model_name = config.get('model_name', self.default_model)
        self.client = anthropic.Client(api_key=self.api_key)
    
    def generate_text(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Generate text using Claude."""
        if not self.client:
            raise RuntimeError("Claude not initialized")
        
        options = options or {}
        temperature = options.get('temperature', 0.7)
        max_tokens = options.get('max_tokens', 1024)
        
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def generate_chat_response(self, messages: List[Dict[str, str]], 
                             options: Optional[Dict[str, Any]] = None) -> str:
        """Generate chat response using Claude."""
        if not self.client:
            raise RuntimeError("Claude not initialized")
        
        options = options or {}
        temperature = options.get('temperature', 0.7)
        max_tokens = options.get('max_tokens', 1024)
        
        # Convert MCP message format to Claude format
        claude_messages = []
        for msg in messages:
            role = "assistant" if msg["role"] == "assistant" else "user"
            claude_messages.append({"role": role, "content": msg["content"]})
        
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=claude_messages
        )
        return message.content[0].text
    
    def analyze_image(self, image_data: bytes, prompt: Optional[str] = None, 
                     options: Optional[Dict[str, Any]] = None) -> str:
        """Analyze an image using Claude."""
        if not self.client:
            raise RuntimeError("Claude not initialized")
        
        options = options or {}
        temperature = options.get('temperature', 0.7)
        max_tokens = options.get('max_tokens', 1024)
        
        # Create message with image
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data.decode('utf-8')
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt or "Please describe this image in detail."
                    }
                ]
            }]
        )
        return message.content[0].text
    
    def moderate_content(self, content: str, 
                        options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Use Claude to check content for policy violations."""
        if not self.client:
            raise RuntimeError("Claude not initialized")
        
        prompt = """Please analyze the following content for potential policy violations. 
        Consider: hate speech, explicit content, violence, harassment, or other harmful content.
        Respond with a JSON object containing:
        - is_flagged (boolean)
        - categories (list of violated categories)
        - explanation (brief explanation)
        
        Content to analyze: {content}"""
        
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            temperature=0,
            messages=[{"role": "user", "content": prompt.format(content=content)}]
        )
        return eval(message.content[0].text)  # Convert string JSON to dict
    
    def embed_text(self, text: str, options: Optional[Dict[str, Any]] = None) -> List[float]:
        """Embedding is not supported by Claude."""
        raise NotImplementedError("Claude does not support native text embeddings")
    
    @property
    def capabilities(self) -> Dict[str, bool]:
        """Return Claude's capabilities."""
        return self._capabilities 