# Multi-Channel Platform (MCP)

A flexible and extensible messaging platform integration service that supports multiple collaboration tools like Slack, Microsoft Teams, and more.

## Features

- Abstract interface for messaging platforms
- Support for multiple platforms simultaneously
- Easy to extend for new platforms
- Handles common events (messages, member joins)
- Configurable through environment variables

## Currently Supported Platforms

- Slack
- Microsoft Teams

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your platform credentials:

   ```env
   # Slack Configuration
   SLACK_BOT_TOKEN=your-slack-bot-token

   # Teams Configuration
   TEAMS_WEBHOOK_URL=your-teams-webhook-url
   TEAMS_TOKEN=your-teams-token

   # General Configuration
   PORT=3000
   DEBUG=false
   ```

## Running the Application

```bash
python -m mcp.app
```

The server will start on port 3000 by default. You can change this by setting the `PORT` environment variable.

## Adding a New Platform

1. Create a new adapter in `mcp/adapters/` that implements the `MessagingPlatform` interface
2. Register the platform in `PlatformFactory`
3. Add configuration handling in `app.py`

Example for adding a new platform:

```python
# 1. Create adapter (e.g., webex_adapter.py)
class WebexAdapter(MessagingPlatform):
    # Implement all required methods
    pass

# 2. Register in platform_factory.py
PlatformFactory.register_platform('webex', WebexAdapter)

# 3. Add configuration in app.py
if os.getenv('WEBEX_TOKEN'):
    webex = PlatformFactory.create_platform('webex')
    webex.initialize({'token': os.getenv('WEBEX_TOKEN')})
    platforms['webex'] = webex
```

## Webhook URLs

Each platform has its own webhook endpoint:

- Slack: `/webhook/slack`
- Teams: `/webhook/teams`

Configure these URLs in your platform's webhook settings.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
