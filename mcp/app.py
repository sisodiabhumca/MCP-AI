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
        try:
            openai = AIModelFactory.create_model('openai')
            openai.initialize({
                'api_key': os.getenv('OPENAI_API_KEY'),
                'model': os.getenv('OPENAI_MODEL', 'gpt-4')
            })
            models['openai'] = openai
        except Exception as e:
            print(f"Warning: Failed to initialize OpenAI: {str(e)}")
            print("Continuing with other models...")
        
    # Initialize Gemini if configured
    if os.getenv('GEMINI_API_KEY'):
        gemini = AIModelFactory.create_model('gemini')
        gemini.initialize({
            'api_key': os.getenv('GEMINI_API_KEY'),
            'model': os.getenv('GEMINI_MODEL', 'gemini-pro')
        })
        models['gemini'] = gemini

    # Initialize Local Llama if configured
    if os.getenv('LOCAL_LLAMA_MODEL_PATH'):
        local_llama = AIModelFactory.create_model('local_llama')
        local_llama.initialize({
            'model_path': os.getenv('LOCAL_LLAMA_MODEL_PATH'),
            'n_gpu_layers': int(os.getenv('LOCAL_LLAMA_N_GPU_LAYERS', '-1')),
            'n_ctx': int(os.getenv('LOCAL_LLAMA_N_CTX', '2048'))
        })
        models['local_llama'] = local_llama

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
            
        result = models[model].generate_text(prompt, options=data.get('options', {}))
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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=3000, help='Port to run the server on')
    args = parser.parse_args()
    
    initialize_models()
    if not models:
        print("Warning: No AI models configured!")
        print("Please set up at least one model's API key in environment variables.")
        return
        
    app.run(port=args.port)
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    app.run(port=port, debug=debug)

if __name__ == '__main__':
    main() 