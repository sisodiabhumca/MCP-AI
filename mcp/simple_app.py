from flask import Flask, request, jsonify
from llama_cpp import Llama
import os
from dotenv import load_dotenv
import sys
import argparse

# Load environment variables
load_dotenv()

app = Flask(__name__)

def initialize_model():
    # Try to get model path from environment variable
    model_path = os.getenv('LOCAL_LLAMA_MODEL_PATH')
    
    # If not set, try to find a .gguf file in common locations
    if not model_path:
        common_paths = [
            os.path.expanduser('~/Downloads'),
            os.path.expanduser('~/models'),
            os.path.expanduser('~/llama-models'),
            os.path.expanduser('~/Documents'),
            os.path.expanduser('~/Desktop')
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith('.gguf'):
                        model_path = os.path.join(path, file)
                        print(f"Found model at: {model_path}")
                        break
            if model_path:
                break
    
    if not model_path:
        print("No model file found. Please set LOCAL_LLAMA_MODEL_PATH environment variable or place a .gguf file in one of the common locations.")
        sys.exit(1)
    
    n_gpu_layers = int(os.getenv('LOCAL_LLAMA_N_GPU_LAYERS', '-1'))
    n_ctx = int(os.getenv('LOCAL_LLAMA_N_CTX', '4096'))  # Increased context window
    
    try:
        llm = Llama(
            model_path=model_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            n_batch=512,  # Increased batch size for better performance
            n_threads=4   # Use multiple threads for processing
        )
        print(f"Successfully loaded model from: {model_path}")
        return llm
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        sys.exit(1)

# Initialize the model
llm = initialize_model()

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    temperature = float(data.get('temperature', 0.7))
    max_tokens = int(data.get('max_tokens', 2048))
    system_prompt = data.get('system_prompt', '')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        # Combine system prompt and user prompt if system prompt is provided
        full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant: " if system_prompt else prompt
        
        response = llm(
            full_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,  # Added top_p for better response quality
            repeat_penalty=1.1,  # Added repeat penalty to avoid repetitive responses
            stop=["User:", "\n\n"]
        )
        return jsonify({
            'response': response['choices'][0]['text'].strip()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    temperature = float(data.get('temperature', 0.7))
    max_tokens = int(data.get('max_tokens', 2048))
    system_prompt = data.get('system_prompt', '')
    
    if not messages:
        return jsonify({'error': 'No messages provided'}), 400
    
    try:
        # Format messages into a prompt
        prompt = f"System: {system_prompt}\n\n" if system_prompt else ""
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            prompt += f"{role.capitalize()}: {content}\n"
        prompt += "Assistant: "
        
        response = llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,  # Added top_p for better response quality
            repeat_penalty=1.1,  # Added repeat penalty to avoid repetitive responses
            stop=["User:", "\n\n"]
        )
        return jsonify({
            'response': response['choices'][0]['text'].strip()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'model_path': os.getenv('LOCAL_LLAMA_MODEL_PATH')
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=None, help='Port to run the server on')
    args, _ = parser.parse_known_args()

    # Priority: CLI arg > env var > default
    port = args.port or int(os.getenv('LLAMA_SERVER_PORT', 5000))
    app.run(host='0.0.0.0', port=port) 