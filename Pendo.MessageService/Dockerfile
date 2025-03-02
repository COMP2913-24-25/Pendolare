FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script and make it executable
COPY entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

# Copy the rest of the application
COPY . .

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Use entrypoint script
CMD ["/app/entrypoint.sh"]
