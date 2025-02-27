FROM python:3.9-slim

# Add build dependencies and debugging tools
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Add websockets to requirements.txt or add it explicitly here
RUN pip install --no-cache-dir -r requirements.txt websockets

# Expose both HTTP and WebSocket ports
EXPOSE 5006
EXPOSE 5007

# Set environment variable for TLS proxy
ENV BEHIND_TLS_PROXY=true

# Run with more verbose output
CMD ["python", "-m", "src.run_servers"]
