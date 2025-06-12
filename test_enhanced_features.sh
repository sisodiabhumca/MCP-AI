#!/bin/bash

echo "=== Testing Health Check ==="
curl http://localhost:5000/health

echo -e "\n\n=== Testing System Prompt ==="
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the best programming language?",
    "system_prompt": "You are a helpful AI assistant that specializes in programming. Always provide balanced, objective answers.",
    "temperature": 0.7
  }'

echo -e "\n\n=== Testing Max Tokens Control ==="
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a detailed explanation of quantum computing",
    "max_tokens": 100,
    "temperature": 0.7
  }'

echo -e "\n\n=== Testing Chat with System Prompt ==="
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is your favorite movie?"},
      {"role": "assistant", "content": "I am an AI assistant and do not have personal preferences."},
      {"role": "user", "content": "Then recommend me a good movie to watch."}
    ],
    "system_prompt": "You are a movie critic AI assistant. Provide thoughtful movie recommendations based on genres and themes.",
    "temperature": 0.7
  }'

echo -e "\n\n=== Testing Long Response with High Max Tokens ==="
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a detailed guide about machine learning algorithms",
    "max_tokens": 4096,
    "temperature": 0.7
  }' 