FROM python:3.9-slim
WORKDIR /app
# Install dependencies:
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the application source code.
COPY . .
# Expose port 8000 which Cloud Run expects.
EXPOSE 8000
# Run the application using uvicorn.
CMD ["python", "main.py"]