# Multi-Channel Platform (MCP) for AI Models

A flexible and extensible AI model integration service that supports multiple AI providers like OpenAI, Google Gemini, and more. This project implements a clean architecture pattern to make it easy to add support for new AI models while maintaining a consistent interface.

## Architecture

The project follows a modular architecture with the following key components:

### Core Components (`mcp/core/`)

1. **AI Interface** (`ai_interface.py`)
   - Defines the abstract base class `AIModel`
   - Specifies required methods for all AI implementations:
     - `initialize()`: Model-specific initialization
     - `generate_text()`: Text generation
     - `generate_chat_response()`: Chat completion
     - `embed_text()`: Text embedding
     - `analyze_image()`: Image analysis
     - `moderate_content()`: Content moderation

2. **AI Factory** (`ai_factory.py`)
   - Implements the Factory pattern for creating AI model instances
   - Maintains a registry of available models
   - Provides methods to:
     - Register new model types
     - Create model instances
     - List available models

### AI Model Adapters (`mcp/adapters/ai/`)

1. **OpenAI Adapter** (`openai_adapter.py`)
   - Implements OpenAI-specific functionality
   - Supports GPT-4, DALL-E, and other OpenAI models
   - Handles all OpenAI API features

2. **Gemini Adapter** (`gemini_adapter.py`)
   - Implements Google Gemini integration
   - Supports Gemini Pro and Gemini Pro Vision
   - Handles all Gemini API features

## Features

### Current Capabilities

1. **Text Generation**
   - Prompt completion
   - Chat conversations
   - Context-aware responses

2. **Image Processing**
   - Image analysis
   - Visual question answering
   - Image description

3. **Advanced Features**
   - Text embeddings
   - Content moderation
   - Model-specific optimizations

## API Endpoints

### Model Information
- `GET /api/models`
  - List all available models and their capabilities

### Text Generation
- `POST /api/[model]/generate`
  ```json
  {
    "prompt": "Your prompt here",
    "options": {
      "temperature": 0.7,
      "max_tokens": 100
    }
  }
  ```

### Chat
- `POST /api/[model]/chat`
  ```json
  {
    "messages": [
      {"role": "user", "content": "Hello"},
      {"role": "assistant", "content": "Hi there!"},
      {"role": "user", "content": "How are you?"}
    ],
    "options": {
      "temperature": 0.7
    }
  }
  ```

### Embeddings
- `POST /api/[model]/embed`
  ```json
  {
    "text": "Text to embed",
    "options": {}
  }
  ```

### Image Analysis
- `POST /api/[model]/analyze-image`
  - Multipart form data:
    - `image`: Image file
    - `prompt`: Optional prompt/question about the image

### Content Moderation
- `POST /api/[model]/moderate`
  ```json
  {
    "content": "Content to moderate"
  }
  ```

## Configuration

### Environment Variables

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4  # Optional

# Google Gemini Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-pro  # Optional

# Server Configuration
PORT=3000
DEBUG=false
```

## Development

### Adding a New AI Model

1. Create new adapter:
```python
class NewModelAdapter(AIModel):
    def __init__(self):
        self.client = None
        self._capabilities = {
            "text_generation": True,
            "chat": True,
            # ... other capabilities
        }
    
    def initialize(self, config):
        # Model-specific initialization
        pass
    
    # Implement other required methods
```

2. Register model:
```python
AIModelFactory.register_model('new_model', NewModelAdapter)
```

3. Add configuration:
```python
if os.getenv('NEW_MODEL_API_KEY'):
    model = AIModelFactory.create_model('new_model')
    model.initialize({'api_key': os.getenv('NEW_MODEL_API_KEY')})
    models['new_model'] = model
```

## Installation and Setup

1. Clone the repository:
```bash
git clone https://github.com/sisodiabhumca/MCP-AI.git
cd MCP-AI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file from template and configure API keys

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
