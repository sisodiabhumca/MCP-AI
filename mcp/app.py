from flask import Flask, request, jsonify
from typing import Dict
import os
from dotenv import load_dotenv

from .core.ai_factory import AIModelFactory
from .core.ai_interface import AIModel

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize AI models
models: Dict[str, AIModel] = {}

def initialize_models():
    """Initialize all configured AI models"""
    # Initialize OpenAI if configured
    if os.getenv('OPENAI_API_KEY'):
        openai = AIModelFactory.create_model('openai')
        openai.initialize({
            'api_key': os.getenv('OPENAI_API_KEY'),
            'model': os.getenv('OPENAI_MODEL', 'gpt-4')
        })
        models['openai'] = openai
        
    # Initialize Gemini if configured
    if os.getenv('GEMINI_API_KEY'):
        gemini = AIModelFactory.create_model('gemini')
        gemini.initialize({
            'api_key': os.getenv('GEMINI_API_KEY'),
            'model': os.getenv('GEMINI_MODEL', 'gemini-pro')
        })
        models['gemini'] = gemini

@app.route('/api/models', methods=['GET'])
def list_models():
    """List all available models and their capabilities"""
    model_info = {}
    for name, model in models.items():
        model_info[name] = model.model_info
    return jsonify(model_info)

@app.route('/api/<model>/generate', methods=['POST'])
def generate_text(model: str):
    """Generate text using specified model"""
    if model not in models:
        return jsonify({'error': f'Model {model} not configured'}), 400
        
    try:
        data = request.json
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
            
        result = models[model].generate_text(prompt, **data.get('options', {}))
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<model>/chat', methods=['POST'])
def chat(model: str):
    """Generate chat response using specified model"""
    if model not in models:
        return jsonify({'error': f'Model {model} not configured'}), 400
        
    try:
        data = request.json
        messages = data.get('messages', [])
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
            
        result = models[model].generate_chat_response(messages, **data.get('options', {}))
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<model>/embed', methods=['POST'])
def embed_text(model: str):
    """Generate embeddings using specified model"""
    if model not in models:
        return jsonify({'error': f'Model {model} not configured'}), 400
        
    try:
        data = request.json
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        result = models[model].embed_text(text, **data.get('options', {}))
        return jsonify({'embedding': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<model>/analyze-image', methods=['POST'])
def analyze_image(model: str):
    """Analyze image using specified model"""
    if model not in models:
        return jsonify({'error': f'Model {model} not configured'}), 400
        
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
            
        image_file = request.files['image']
        image_data = image_file.read()
        prompt = request.form.get('prompt')
        
        result = models[model].analyze_image(image_data, prompt)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/<model>/moderate', methods=['POST'])
def moderate_content(model: str):
    """Moderate content using specified model"""
    if model not in models:
        return jsonify({'error': f'Model {model} not configured'}), 400
        
    try:
        data = request.json
        content = data.get('content')
        if not content:
            return jsonify({'error': 'No content provided'}), 400
            
        result = models[model].moderate_content(content)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Main application entry point"""
    initialize_models()
    
    if not models:
        print("Warning: No AI models configured!")
        print("Please set up at least one model's API key in environment variables.")
        return
        
    port = int(os.getenv('PORT', '3000'))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    app.run(port=port, debug=debug)

if __name__ == '__main__':
    main() 