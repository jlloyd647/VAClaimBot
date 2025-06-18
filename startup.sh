#!/bin/bash

# Start the Ollama model server in the background
ollama serve &

# Wait a moment to ensure it's fully running
echo "🟡 Waiting for Ollama to start..."
sleep 3

# Pull the model (this only pulls if it's not already cached)
echo "⬇️ Pulling tinyllama model..."
ollama pull tinyllama

# Start Streamlit
echo "🚀 Starting Streamlit app..."
streamlit run app.py --server.port=10000 --server.enableCORS false
