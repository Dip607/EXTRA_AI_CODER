# Dockerfile

FROM python:3.11-slim

# Install system dependencies (Tesseract and PDF tools)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    && apt-get clean

# Set workdir
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Expose the port Django runs on
EXPOSE 8000

# Run Django dev server (you can replace with gunicorn in prod)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
