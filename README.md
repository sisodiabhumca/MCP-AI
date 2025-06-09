# MCP Slack Server

A Python-based MCP server that integrates with Slack for real-time communication and collaboration.

## Features

- Real-time message handling
- Webhook integration with Slack
- Member join notifications
- Custom message processing
- Extensible architecture

## Prerequisites

- Python 3.8+
- Slack workspace
- Slack Bot Token

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the root directory with your Slack Bot Token:
```
SLACK_BOT_TOKEN=xoxb-your-bot-token
```

2. Get your Slack Bot Token by:
   - Going to https://api.slack.com/apps
   - Creating a new app or selecting an existing one
   - Under "OAuth & Permissions", install the app to your workspace
   - Copy the Bot User OAuth Token

## Running the Server

1. Start the server:
```bash
python mcp_slack_server.py
```

2. The server will run on `http://localhost:3000`

## Webhook Setup

1. In your Slack app configuration:
   - Go to "Event Subscriptions"
   - Enable Events
   - Add Request URL: `http://your-server-url/webhook`
   - Subscribe to bot events:
     - `message.channels`
     - `member_joined_channel`

## Extending the Server

To add new functionality:

1. Add new event handlers in `mcp_slack_server.py`
2. Implement custom message processing in `handle_message()`
3. Add new webhook endpoints as needed

## Error Handling

The server includes basic error handling for:
- Slack API errors
- Webhook processing errors
- Message sending failures

## Security

- Keep your Slack Bot Token secure
- Never commit your `.env` file
- Consider using environment variables in production

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
