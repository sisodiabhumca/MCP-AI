from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Dict, Any, Optional

from ..core.platform_interface import MessagingPlatform

class SlackAdapter(MessagingPlatform):
    """Slack implementation of the messaging platform interface"""
    
    def __init__(self):
        self.client = None
        
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the Slack client with configuration"""
        self.client = WebClient(token=config.get('token'))
        
    def send_message(self, channel_id: str, message: str, **kwargs) -> bool:
        """Send a message to a Slack channel"""
        try:
            self.client.chat_postMessage(
                channel=channel_id,
                text=message,
                **kwargs
            )
            return True
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
            return False
            
    def handle_webhook(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming Slack webhook events"""
        try:
            event = payload.get('event', {})
            event_type = event.get('type')
            
            if event_type == 'message':
                self.handle_message(event)
            elif event_type == 'member_joined_channel':
                self.handle_member_join(event)
                
            return {'status': 'success'}
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return {'status': 'error', 'message': str(e)}
            
    def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """Get information about a Slack user"""
        try:
            response = self.client.users_info(user=user_id)
            return response['user']
        except SlackApiError as e:
            print(f"Error getting user info: {e.response['error']}")
            return {}
            
    def handle_message(self, event: Dict[str, Any]) -> None:
        """Handle incoming Slack messages"""
        try:
            user_id = event.get('user')
            text = event.get('text', '')
            channel_id = event.get('channel')
            
            if "help" in text.lower():
                self.send_message(channel_id, "I'm here to help! Type commands to interact with me.")
                
        except Exception as e:
            print(f"Error handling message: {str(e)}")
            
    def handle_member_join(self, event: Dict[str, Any]) -> None:
        """Handle when a new member joins a Slack channel"""
        try:
            user_id = event.get('user')
            channel_id = event.get('channel')
            
            user_info = self.get_user_info(user_id)
            user_name = user_info.get('name', 'new member')
            
            self.send_message(channel_id, f"Welcome to the channel, @{user_name}!")
            
        except Exception as e:
            print(f"Error handling member join: {str(e)}") 