# Multi-Channel Platform (MCP)

A flexible and extensible messaging platform integration service that supports multiple collaboration tools like Slack, Microsoft Teams, and more. This project implements a clean architecture pattern to make it easy to add support for new messaging platforms while maintaining a consistent interface.

## Architecture

The project follows a modular architecture with the following key components:

### Core Components (`mcp/core/`)

1. **Platform Interface** (`platform_interface.py`)
   - Defines the abstract base class `MessagingPlatform`
   - Specifies required methods for all platform implementations:
     - `initialize()`: Platform-specific initialization
     - `send_message()`: Message sending
     - `handle_webhook()`: Webhook event processing
     - `get_user_info()`: User information retrieval
     - `handle_message()`: Message event handling
     - `handle_member_join()`: Member join event handling

2. **Platform Factory** (`platform_factory.py`)
   - Implements the Factory pattern for creating platform instances
   - Maintains a registry of available platforms
   - Provides methods to:
     - Register new platform types
     - Create platform instances
     - Manage platform configurations

### Platform Adapters (`mcp/adapters/`)

1. **Slack Adapter** (`slack_adapter.py`)
   - Implements Slack-specific functionality
   - Uses `slack_sdk` for API interactions
   - Handles Slack events and message formats

2. **Teams Adapter** (`teams_adapter.py`)
   - Implements Microsoft Teams integration
   - Uses Microsoft Graph API
   - Handles Teams-specific events and message formats

### Main Application (`mcp/app.py`)

- Flask-based web application
- Dynamic platform initialization
- Webhook routing and handling
- Environment-based configuration

## Technical Implementation

### Platform Interface

```python
class MessagingPlatform(ABC):
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def send_message(self, channel_id: str, message: str, **kwargs) -> bool:
        pass

    # ... other abstract methods
```

### Platform Factory

```python
class PlatformFactory:
    _platforms: Dict[str, Type[MessagingPlatform]] = {
        'slack': SlackAdapter,
        'teams': TeamsAdapter
    }

    @classmethod
    def create_platform(cls, platform_type: str) -> MessagingPlatform:
        if platform_type not in cls._platforms:
            raise ValueError(f"Unknown platform type: {platform_type}")
        return cls._platforms[platform_type]()
```

## Features

### Current Capabilities

1. **Multi-Platform Support**
   - Simultaneous support for multiple messaging platforms
   - Platform-specific webhook endpoints
   - Unified message handling interface

2. **Event Handling**
   - Message events
   - Member join notifications
   - Platform-specific custom events

3. **Configuration Management**
   - Environment-based configuration
   - Platform-specific settings
   - Dynamic platform initialization

### Extensibility

The system is designed for easy extension:

1. **Adding New Platforms**
   - Create new adapter class
   - Implement MessagingPlatform interface
   - Register with PlatformFactory
   - Add configuration in app.py

2. **Custom Event Types**
   - Extend platform adapters
   - Add new event handlers
   - Implement platform-specific logic

## Configuration

### Environment Variables

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

### Webhook Endpoints

- Slack: `/webhook/slack`
- Teams: `/webhook/teams`
- New platforms: `/webhook/<platform-name>`

## Development

### Adding a New Platform

1. Create new adapter:
```python
class NewPlatformAdapter(MessagingPlatform):
    def __init__(self):
        self.client = None
    
    def initialize(self, config):
        # Platform-specific initialization
        pass
    
    # Implement other required methods
```

2. Register platform:
```python
PlatformFactory.register_platform('new_platform', NewPlatformAdapter)
```

3. Add configuration:
```python
if os.getenv('NEW_PLATFORM_TOKEN'):
    platform = PlatformFactory.create_platform('new_platform')
    platform.initialize({'token': os.getenv('NEW_PLATFORM_TOKEN')})
    platforms['new_platform'] = platform
```

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/sisodiabhumca/MCP-Collab.git
cd MCP-Collab
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`

4. Run the application:
```bash
python -m mcp.app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
