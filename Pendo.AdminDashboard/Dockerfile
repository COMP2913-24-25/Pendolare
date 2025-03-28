FROM python:3.9-slim

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 5000

# Run gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
