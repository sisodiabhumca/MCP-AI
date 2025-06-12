#!/bin/bash

# Create models directory
mkdir -p models

# Download the model
echo "Downloading Llama 2 7B Chat model..."
curl -L "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf" -o models/llama-2-7b-chat.Q4_K_M.gguf

# Check if download was successful
if [ $? -eq 0 ]; then
    echo "Download completed successfully!"
    echo "Model saved to: models/llama-2-7b-chat.Q4_K_M.gguf"
else
    echo "Download failed. Please try again."
fi 