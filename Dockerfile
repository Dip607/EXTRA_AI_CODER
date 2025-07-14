# Use slim python image
FROM python:3.11-slim

# Install required system dependencies including Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Run Django using Gunicorn
CMD ["gunicorn", "code_forum.wsgi:application", "--bind", "0.0.0.0:8000"]
