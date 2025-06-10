from typing import Dict, Any, Optional
import time
from threading import Lock
from collections import deque

class RateLimiter:
    """Rate limiter for API calls"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window_size = 60  # 1 minute in seconds
        self.requests = deque()
        self.lock = Lock()
        
    def wait_if_needed(self) -> None:
        """Wait if rate limit is exceeded"""
        with self.lock:
            now = time.time()
            
            # Remove old requests
            while self.requests and self.requests[0] < now - self.window_size:
                self.requests.popleft()
            
            # If we've hit the limit, wait
            if len(self.requests) >= self.requests_per_minute:
                sleep_time = self.requests[0] - (now - self.window_size)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            # Add current request
            self.requests.append(now)

class ModelRateLimiter:
    """Rate limiter for specific AI models"""
    
    _limiters: Dict[str, RateLimiter] = {
        'openai': RateLimiter(requests_per_minute=60),  # OpenAI default limit
        'gemini': RateLimiter(requests_per_minute=60),  # Gemini default limit
    }
    
    @classmethod
    def register_model(cls, model: str, requests_per_minute: int) -> None:
        """Register a new model with its rate limit"""
        cls._limiters[model] = RateLimiter(requests_per_minute)
    
    @classmethod
    def wait_if_needed(cls, model: str) -> None:
        """Wait if needed for the specified model"""
        if model in cls._limiters:
            cls._limiters[model].wait_if_needed()
            
    @classmethod
    def get_limiter(cls, model: str) -> Optional[RateLimiter]:
        """Get rate limiter for a specific model"""
        return cls._limiters.get(model) 