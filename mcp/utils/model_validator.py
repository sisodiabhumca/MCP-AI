from typing import Dict, Any, List, Optional
import re

class ModelValidator:
    """Validator for AI model inputs and configurations"""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate API key format"""
        if not api_key:
            return False
        return True
    
    @staticmethod
    def validate_chat_messages(messages: List[Dict[str, str]]) -> bool:
        """Validate chat message format"""
        if not messages:
            return False
            
        required_keys = {'role', 'content'}
        valid_roles = {'user', 'assistant', 'system'}
        
        for message in messages:
            if not isinstance(message, dict):
                return False
            if not all(key in message for key in required_keys):
                return False
            if message['role'] not in valid_roles:
                return False
            if not isinstance(message['content'], str):
                return False
                
        return True
    
    @staticmethod
    def validate_image_data(image_data: bytes, max_size_mb: int = 10) -> bool:
        """Validate image data"""
        if not image_data:
            return False
            
        # Check file size (max 10MB by default)
        if len(image_data) > max_size_mb * 1024 * 1024:
            return False
            
        return True
    
    @staticmethod
    def validate_model_options(options: Dict[str, Any], model: str) -> Dict[str, Any]:
        """Validate and sanitize model options"""
        valid_options = {
            'temperature': lambda x: isinstance(x, (int, float)) and 0 <= x <= 2,
            'max_tokens': lambda x: isinstance(x, int) and x > 0,
            'top_p': lambda x: isinstance(x, (int, float)) and 0 <= x <= 1,
            'frequency_penalty': lambda x: isinstance(x, (int, float)) and -2 <= x <= 2,
            'presence_penalty': lambda x: isinstance(x, (int, float)) and -2 <= x <= 2
        }
        
        sanitized = {}
        for key, value in options.items():
            if key in valid_options and valid_options[key](value):
                sanitized[key] = value
                
        return sanitized
    
    @staticmethod
    def validate_prompt(prompt: str, max_length: int = 4096) -> bool:
        """Validate prompt text"""
        if not prompt or not isinstance(prompt, str):
            return False
            
        if len(prompt) > max_length:
            return False
            
        return True
    
    @staticmethod
    def sanitize_prompt(prompt: str) -> str:
        """Sanitize prompt text"""
        # Remove null bytes
        prompt = prompt.replace('\x00', '')
        
        # Remove excessive whitespace
        prompt = ' '.join(prompt.split())
        
        # Remove potentially harmful characters
        prompt = re.sub(r'[^\w\s\.,!?\'"-]', '', prompt)
        
        return prompt.strip() 