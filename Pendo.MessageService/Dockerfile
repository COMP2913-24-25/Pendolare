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

# Command to run when the container starts
CMD ["python", "-m", "src.run_servers"]