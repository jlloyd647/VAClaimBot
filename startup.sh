#!/bin/bash

# Start the Ollama model server in the background
echo "🧠 Starting Ollama..."
ollama serve &

# Wait a few seconds to ensure Ollama is up
echo "⏳ Waiting for Ollama to fully start..."
sleep 3

# Pull the mistral model (will skip if already cached)
echo "⬇️ Pulling mistral model..."
ollama pull mistral

# Start the Streamlit app
echo "🚀 Launching Streamlit..."
streamlit run app.py --server.port=10000 --server.enableCORS false