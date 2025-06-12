from typing import Dict, List, Optional, Any
from mcp.core.ai_interface import AIModel
from llama_cpp import Llama
import os

class LocalLlamaAdapter(AIModel):
    """Adapter for running Llama models locally using llama.cpp."""
    
    def __init__(self):
        self.llm = None
        self._capabilities = {
            "text_generation": True,
            "chat": True,
            "embeddings": True,
            "image_analysis": False,
            "moderation": False
        }
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize local Llama model."""
        model_path = config.get('model_path')
        if not model_path or not os.path.exists(model_path):
            raise ValueError(f"Model path not found: {model_path}")
        
        n_ctx = config.get('n_ctx', 2048)
        
        print(f"Initializing Llama model from: {model_path}")
        print(f"Context size: {n_ctx}")
        
        try:
            # Initialize with basic configuration
            self.llm = Llama(
                model_path=model_path,
                n_ctx=n_ctx,
                verbose=True,
                n_threads=4,     # Use multiple threads
                n_batch=512,     # Process 512 tokens at a time
                use_mmap=False,  # Disable memory mapping
                use_mlock=True,  # Lock memory to prevent swapping
                n_gpu_layers=0,  # Force CPU usage
                logits_all=True, # Return all logits
            )
            
            # Test the model initialization
            test_prompt = "Hello"
            print(f"Testing model with prompt: {test_prompt}")
            test_output = self.llm(
                test_prompt,
                max_tokens=1,
                temperature=0.0,
                echo=False,
                logprobs=1,      # Get log probabilities
                top_p=1.0,       # Use all tokens
                top_k=0          # No top-k filtering
            )
            print(f"Test output: {test_output}")
            
            print("Llama model initialized and tested successfully")
        except Exception as e:
            print(f"Error initializing Llama model: {str(e)}")
            raise RuntimeError("Local Llama not initialized")
    
    def generate_text(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Generate text using local Llama."""
        if not self.llm:
            raise RuntimeError("Local Llama not initialized")
        
        options = options or {}
        max_tokens = options.get('max_tokens', 1024)
        temperature = options.get('temperature', 0.7)
        
        # Convert to llama.cpp format
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        
        # Convert messages to llama.cpp format
        formatted_prompt = "".join([
            f"{msg['role']}: {msg['content']}\n" 
            for msg in messages
        ])
        
        output = self.llm(
            formatted_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            echo=False
        )
        
        return output['choices'][0]['text']
    
    def generate_chat_response(self, messages: List[Dict[str, str]], 
                             options: Optional[Dict[str, Any]] = None) -> str:
        """Generate chat response using local Llama."""
        if not self.llm:
            raise RuntimeError("Local Llama not initialized")
        
        # Format messages in chat format
        formatted_prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                formatted_prompt += f"### System:\n{content}\n\n"
            elif role == "user":
                formatted_prompt += f"### User:\n{content}\n\n"
            elif role == "assistant":
                formatted_prompt += f"### Assistant:\n{content}\n\n"
        
        formatted_prompt += "### Assistant:\n"
        return self.generate_text(formatted_prompt, options)
    
    def embed_text(self, text: str, options: Optional[Dict[str, Any]] = None) -> List[float]:
        """Generate embeddings using local Llama."""
        if not self.llm:
            raise RuntimeError("Local Llama not initialized")
        
        embeddings = self.llm.embed(text)
        return embeddings.tolist()
    
    def analyze_image(self, image_data: bytes, prompt: Optional[str] = None, 
                     options: Optional[Dict[str, Any]] = None) -> str:
        """Image analysis is not supported by local Llama."""
        raise NotImplementedError("Local Llama does not support image analysis")
    
    def moderate_content(self, content: str, 
                        options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Content moderation is not supported by local Llama."""
        raise NotImplementedError("Local Llama does not support content moderation")
    
    @property
    def capabilities(self) -> Dict[str, bool]:
        """Return local Llama's capabilities."""
        return self._capabilities 

    @property
    def model_info(self) -> Dict[str, Any]:
        """Return information about the local Llama model."""
        return {
            "provider": "Local Llama (llama.cpp)",
            "model": getattr(self.llm, 'model_path', 'unknown') if self.llm else 'uninitialized',
            "type": "Local Large Language Model",
            "capabilities": self.capabilities
        } 