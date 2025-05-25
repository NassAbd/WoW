# Backend Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the backend
COPY backend/ .

# Expose port for Flask (default 5000)
EXPOSE 5000

# Use .env if needed
ENV FLASK_ENV=development

CMD ["python", "app.py"]
