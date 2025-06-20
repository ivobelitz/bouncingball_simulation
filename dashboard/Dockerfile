# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    numpy==1.24.3 \
    matplotlib==3.7.1 \
    pandas==2.0.3 \
    requests==2.31.0 \
    flask==2.3.3 \
    werkzeug==2.3.7 \
    flask-cors==4.0.0 \
    plotly==5.15.0

# Copy the dashboard application
COPY dashboard.py .
COPY templates/ templates/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port the dashboard runs on
EXPOSE 5000

# Command to run the dashboard with proper host binding for Docker
CMD ["python", "dashboard.py"]