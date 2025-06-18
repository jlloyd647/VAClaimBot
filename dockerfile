FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pull your preferred model (optional for faster startup)
RUN ollama pull llama3

# Set working directory
WORKDIR /app
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Start Ollama + Streamlit in one container
CMD ollama serve & streamlit run app.py --server.port=10000 --server.enableCORS false
