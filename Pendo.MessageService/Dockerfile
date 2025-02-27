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

# Copy the source code and debug scripts
COPY src/ ./src/
COPY azure_debug.py .

# Print directory contents for debugging
RUN echo "Contents of /app:" && ls -la /app && \
    echo "Contents of /app/src:" && ls -la /app/src

# Verify the debug script exists
RUN test -f ./azure_debug.py || (echo "ERROR: azure_debug.py is missing!" && exit 1)

# Expose both HTTP and WebSocket ports
EXPOSE 5006
EXPOSE 5007

# Run with more verbose output
CMD ["python", "-m", "src.run_servers"]
