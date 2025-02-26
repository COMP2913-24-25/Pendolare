FROM python:3.9-slim

WORKDIR /app

# Install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add aiohttp for the HTTP server
RUN pip install aiohttp

# Copy the rest of the application
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=DEBUG
ENV HTTP_PORT=5007

# Expose both the WebSocket port and HTTP port
EXPOSE 5006 5007

# Command to run the application
CMD ["python", "src/app.py"]
