from flask import Flask, request, jsonify
from typing import Dict
import os
from dotenv import load_dotenv

from .core.platform_factory import PlatformFactory
from .core.platform_interface import MessagingPlatform

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize platforms
platforms: Dict[str, MessagingPlatform] = {}

def initialize_platforms():
    """Initialize all configured platforms"""
    # Initialize Slack if configured
    if os.getenv('SLACK_BOT_TOKEN'):
        slack = PlatformFactory.create_platform('slack')
        slack.initialize({'token': os.getenv('SLACK_BOT_TOKEN')})
        platforms['slack'] = slack
        
    # Initialize Teams if configured
    if os.getenv('TEAMS_WEBHOOK_URL') and os.getenv('TEAMS_TOKEN'):
        teams = PlatformFactory.create_platform('teams')
        teams.initialize({
            'webhook_url': os.getenv('TEAMS_WEBHOOK_URL'),
            'token': os.getenv('TEAMS_TOKEN')
        })
        platforms['teams'] = teams

@app.route('/webhook/<platform>', methods=['POST'])
def webhook(platform: str):
    """Handle webhooks for different platforms"""
    if platform not in platforms:
        return jsonify({'error': f'Platform {platform} not configured'}), 400
        
    try:
        result = platforms[platform].handle_webhook(request.json)
        return jsonify(result or {'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Main application entry point"""
    initialize_platforms()
    
    if not platforms:
        print("Warning: No messaging platforms configured!")
        print("Please set up at least one platform's environment variables.")
        return
        
    port = int(os.getenv('PORT', '3000'))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    app.run(port=port, debug=debug)

if __name__ == '__main__':
    main() 