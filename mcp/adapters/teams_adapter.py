from typing import Dict, Any, Optional
import requests

from ..core.platform_interface import MessagingPlatform

class TeamsAdapter(MessagingPlatform):
    """Microsoft Teams implementation of the messaging platform interface"""
    
    def __init__(self):
        self.webhook_url = None
        self.token = None
        self.base_url = "https://graph.microsoft.com/v1.0"
        
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the Teams client with configuration"""
        self.webhook_url = config.get('webhook_url')
        self.token = config.get('token')
        
    def send_message(self, channel_id: str, message: str, **kwargs) -> bool:
        """Send a message to a Teams channel"""
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'content': message,
                **kwargs
            }
            
            response = requests.post(self.webhook_url, json=payload, headers=headers)
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return False
            
    def handle_webhook(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming Teams webhook events"""
        try:
            event_type = payload.get('type', '')
            
            if event_type == 'message':
                self.handle_message(payload)
            elif event_type == 'memberAdded':
                self.handle_member_join(payload)
                
            return {'status': 'success'}
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return {'status': 'error', 'message': str(e)}
            
    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get information about a Teams user"""
        try:
            headers = {'Authorization': f'Bearer {self.token}'}
            response = requests.get(f"{self.base_url}/users/{user_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting user info: {str(e)}")
            return {}
            
    def handle_message(self, event: Dict[str, Any]) -> None:
        """Handle incoming Teams messages"""
        try:
            user_id = event.get('from', {}).get('id')
            text = event.get('text', '')
            channel_id = event.get('channelId')
            
            if "help" in text.lower():
                self.send_message(channel_id, "I'm here to help! Type commands to interact with me.")
                
        except Exception as e:
            print(f"Error handling message: {str(e)}")
            
    def handle_member_join(self, event: Dict[str, Any]) -> None:
        """Handle when a new member joins a Teams channel"""
        try:
            members_added = event.get('membersAdded', [])
            channel_id = event.get('channelId')
            
            for member in members_added:
                user_id = member.get('id')
                user_info = self.get_user_info(user_id)
                user_name = user_info.get('displayName', 'new member')
                
                self.send_message(channel_id, f"Welcome to the channel, {user_name}!")
                
        except Exception as e:
            print(f"Error handling member join: {str(e)}") 