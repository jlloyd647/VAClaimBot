FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set up app
WORKDIR /app
COPY . .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Add and prepare startup script
COPY startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Add Streamlit config for MIME and headless mode
RUN mkdir -p /app/.streamlit && echo "\
[server]\n\
headless = true\n\
port = 10000\n\
enableCORS = false\n\
enableStaticServing = true\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
" > /app/.streamlit/config.toml

# Run everything via startup script
CMD ["/app/startup.sh"]
