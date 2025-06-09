import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        event = data.get('event', {})
        
        # Handle different types of Slack events
        event_type = event.get('type')
        
        if event_type == 'message':
            handle_message(event)
        elif event_type == 'member_joined_channel':
            handle_member_join(event)
        
        return '', 200
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return '', 500

def handle_message(event):
    """Handle incoming messages from Slack"""
    try:
        user_id = event.get('user')
        text = event.get('text')
        channel_id = event.get('channel')
        
        # Add your message handling logic here
        # For example, you could respond to specific keywords
        if "help" in text.lower():
            send_message(channel_id, "I'm here to help! Type commands to interact with me.")
            
    except Exception as e:
        print(f"Error handling message: {str(e)}")

def handle_member_join(event):
    """Handle when a new member joins a channel"""
    try:
        user_id = event.get('user')
        channel_id = event.get('channel')
        
        # Get user info
        user_info = client.users_info(user=user_id)
        user_name = user_info['user']['name']
        
        # Welcome message
        send_message(channel_id, f"Welcome to the channel, @{user_name}!")
        
    except Exception as e:
        print(f"Error handling member join: {str(e)}")

def send_message(channel_id, message):
    """Send a message to a Slack channel"""
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=message
        )
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

if __name__ == '__main__':
    app.run(port=3000, debug=True)
