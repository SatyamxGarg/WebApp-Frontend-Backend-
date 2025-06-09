# Use Python Alpine base image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Install dependencies for Alpine-based Python, including Poppler
RUN apk add --no-cache \
    gcc musl-dev libffi-dev \
    poppler poppler-utils

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY main.py /app

# Expose backend port
EXPOSE 9000

# Command to run the application
CMD ["uvicorn", "main:app", "--reload", "--port", "9000", "--host", "0.0.0.0"]
