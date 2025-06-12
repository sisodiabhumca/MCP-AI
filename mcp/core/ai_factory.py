from typing import Dict, Type

from ..core.ai_interface import AIModel
from ..adapters.ai.openai_adapter import OpenAIAdapter
from ..adapters.ai.gemini_adapter import GeminiAdapter
from ..adapters.ai.local_llama_adapter import LocalLlamaAdapter

class AIModelFactory:
    """Factory class for creating AI model instances"""
    
    _models: Dict[str, Type[AIModel]] = {
        'openai': OpenAIAdapter,
        'gemini': GeminiAdapter,
        'local_llama': LocalLlamaAdapter
    }
    
    @classmethod
    def register_model(cls, name: str, model_class: Type[AIModel]) -> None:
        """Register a new AI model type"""
        cls._models[name] = model_class
    
    @classmethod
    def create_model(cls, model_type: str) -> AIModel:
        """Create a new AI model instance"""
        if model_type not in cls._models:
            raise ValueError(f"Unknown model type: {model_type}")
            
        return cls._models[model_type]()
    
    @classmethod
    def list_available_models(cls) -> Dict[str, Type[AIModel]]:
        """Return a dictionary of available models"""
        return cls._models.copy() 