#!/bin/bash

echo "=== Testing Basic Generation ==="
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is artificial intelligence?", "temperature": 0.7}'

echo -e "\n\n=== Testing Different Temperature Settings ==="
echo "Low temperature (0.2):"
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a short poem about technology", "temperature": 0.2}'

echo -e "\nHigh temperature (0.9):"
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a short poem about technology", "temperature": 0.9}'

echo -e "\n\n=== Testing Chat Functionality ==="
echo "Simple chat:"
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello, I am a developer."},
      {"role": "assistant", "content": "Hello! Nice to meet you. What kind of development do you do?"},
      {"role": "user", "content": "I work with AI and machine learning."}
    ],
    "temperature": 0.7
  }'

echo -e "\n\n=== Testing Error Handling ==="
echo "Empty prompt:"
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "", "temperature": 0.7}'

echo -e "\nEmpty messages:"
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [], "temperature": 0.7}'

echo -e "\n\n=== Testing Long Context ==="
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a detailed explanation of how neural networks work, including the concepts of layers, activation functions, and backpropagation.",
    "temperature": 0.7
  }'

echo -e "\n\n=== Testing Code Generation ==="
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function that implements binary search.",
    "temperature": 0.7
  }'

echo -e "\n\n=== Testing Multi-turn Technical Discussion ==="
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is the difference between REST and GraphQL?"},
      {"role": "assistant", "content": "REST is a resource-based architecture that uses HTTP methods to perform operations on resources, while GraphQL is a query language that allows clients to request exactly the data they need."},
      {"role": "user", "content": "Can you give me an example of when to use each?"}
    ],
    "temperature": 0.7
  }' 