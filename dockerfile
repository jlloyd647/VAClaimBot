FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Runtime: start Ollama and Streamlit, and pull model on demand if needed
CMD ollama serve & streamlit run app.py --server.port=10000 --server.enableCORS false
