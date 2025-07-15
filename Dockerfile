# Dockerfile

FROM python:3.11-slim

# Prevent prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install Tesseract and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000
# Collect static (optional)
RUN python manage.py collectstatic --noinput

# Run the server
CMD ["gunicorn", "code_forum.wsgi:application", "--bind", "0.0.0.0:8000"]
