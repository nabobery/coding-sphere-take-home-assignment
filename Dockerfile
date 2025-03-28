FROM python:3.9-slim
WORKDIR /app
# Install dependencies:
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client libpq-dev build-essential && \
    pip install --no-cache-dir -r requirements.txt
# Copy the application source code.
COPY . .
# Expose port 8080 which Cloud Run expects.
EXPOSE 8080
# Run the application using uvicorn.
CMD ["python", "main.py"]