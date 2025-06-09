from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class MessagingPlatform(ABC):
    """Abstract base class for messaging platform implementations"""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the platform with configuration"""
        pass
    
    @abstractmethod
    def send_message(self, channel_id: str, message: str, **kwargs) -> bool:
        """Send a message to a channel"""
        pass
    
    @abstractmethod
    def handle_webhook(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming webhook events"""
        pass
    
    @abstractmethod
    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get information about a user"""
        pass
    
    @abstractmethod
    def handle_message(self, event: Dict[str, Any]) -> None:
        """Handle incoming message events"""
        pass
    
    @abstractmethod
    def handle_member_join(self, event: Dict[str, Any]) -> None:
        """Handle member join events"""
        pass 