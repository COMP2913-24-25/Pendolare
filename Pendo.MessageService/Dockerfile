FROM python:3.9-slim

# Set working directory to the project root
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make the directory accessible to Python's import system
ENV PYTHONPATH=/app
ENV WS_PORT=5006
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=DEBUG

# Command to run when the container starts
CMD ["python", "-m", "src.run_servers"]

# Health check to verify service is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${WS_PORT}/health || exit 1