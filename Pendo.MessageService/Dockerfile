FROM python:3.9-slim

WORKDIR /src

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Command to run when the container starts
CMD ["python", "src/run_servers.py"]