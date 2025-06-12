from typing import Dict, List, Optional, Any
from mcp.core.ai_interface import AIModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

class Llama2Adapter(AIModel):
    """Adapter for Meta's Llama 2 models using Hugging Face transformers."""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self._capabilities = {
            "text_generation": True,
            "chat": True,
            "embeddings": True,
            "image_analysis": False,
            "moderation": False
        }
        self.default_model = "meta-llama/Llama-2-7b-chat-hf"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize Llama 2 model."""
        self.model_name = config.get('model_name', self.default_model)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=config.get('hf_token'))
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            token=config.get('hf_token'),
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        # Create text generation pipeline
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
        )
    
    def generate_text(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
        """Generate text using Llama 2."""
        if not self.pipeline:
            raise RuntimeError("Llama 2 not initialized")
        
        options = options or {}
        max_length = options.get('max_tokens', 1024)
        temperature = options.get('temperature', 0.7)
        
        response = self.pipeline(
            prompt,
            max_length=max_length,
            temperature=temperature,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        return response[0]['generated_text'][len(prompt):]
    
    def generate_chat_response(self, messages: List[Dict[str, str]], 
                             options: Optional[Dict[str, Any]] = None) -> str:
        """Generate chat response using Llama 2."""
        if not self.pipeline:
            raise RuntimeError("Llama 2 not initialized")
        
        # Format messages in Llama 2 chat format
        formatted_prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                formatted_prompt += f"<s>[INST] <<SYS>>{content}<</SYS>>\n\n"
            elif role == "user":
                formatted_prompt += f"[INST] {content} [/INST]"
            elif role == "assistant":
                formatted_prompt += f"{content} </s>"
        
        return self.generate_text(formatted_prompt, options)
    
    def embed_text(self, text: str, options: Optional[Dict[str, Any]] = None) -> List[float]:
        """Generate text embeddings using Llama 2's hidden states."""
        if not self.model or not self.tokenizer:
            raise RuntimeError("Llama 2 not initialized")
        
        # Tokenize input text
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get model's hidden states
        with torch.no_grad():
            outputs = self.model(**inputs, output_hidden_states=True)
            
        # Use the last hidden state's CLS token as embedding
        last_hidden_state = outputs.hidden_states[-1]
        embedding = last_hidden_state[0, 0, :].cpu().numpy().tolist()
        
        return embedding
    
    def analyze_image(self, image_data: bytes, prompt: Optional[str] = None, 
                     options: Optional[Dict[str, Any]] = None) -> str:
        """Image analysis is not supported by Llama 2."""
        raise NotImplementedError("Llama 2 does not support image analysis")
    
    def moderate_content(self, content: str, 
                        options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Content moderation is not supported by Llama 2."""
        raise NotImplementedError("Llama 2 does not support content moderation")
    
    @property
    def capabilities(self) -> Dict[str, bool]:
        """Return Llama 2's capabilities."""
        return self._capabilities 