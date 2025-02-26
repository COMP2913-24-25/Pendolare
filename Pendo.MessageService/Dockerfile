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
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Print directory contents for debugging
RUN echo "Contents of /app:" && ls -la /app && \
    echo "Contents of /app/src:" && ls -la /app/src

# Verify the test client exists
RUN test -f ./src/test-client.html || (echo "ERROR: test-client.html is missing!" && exit 1)

# Expose both HTTP and WebSocket ports
EXPOSE 5006
EXPOSE 5007

# Run with more verbose output
CMD ["python", "-m", "src.run_servers"]
