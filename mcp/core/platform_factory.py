from typing import Dict, Type

from ..core.platform_interface import MessagingPlatform
from ..adapters.slack_adapter import SlackAdapter
from ..adapters.teams_adapter import TeamsAdapter

class PlatformFactory:
    """Factory class for creating messaging platform instances"""
    
    _platforms: Dict[str, Type[MessagingPlatform]] = {
        'slack': SlackAdapter,
        'teams': TeamsAdapter
    }
    
    @classmethod
    def register_platform(cls, name: str, platform_class: Type[MessagingPlatform]) -> None:
        """Register a new platform type"""
        cls._platforms[name] = platform_class
    
    @classmethod
    def create_platform(cls, platform_type: str) -> MessagingPlatform:
        """Create a new platform instance"""
        if platform_type not in cls._platforms:
            raise ValueError(f"Unknown platform type: {platform_type}")
            
        return cls._platforms[platform_type]() 