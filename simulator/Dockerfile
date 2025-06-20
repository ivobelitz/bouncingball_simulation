# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for FMU simulation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
RUN pip install fmpy==0.3.25 \
    numpy==2.3.0 \
    pandas==2.3.0 \
    matplotlib==3.10.3 \
    flask==3.1.1 \
    flask-cors==6.0.1
# Copy the simulator files
COPY simulator.py .
COPY bouncingBall.fmu .

# Create output directory for CSV files
RUN mkdir -p /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port the web server runs on
EXPOSE 8000

# Run as web server by default
CMD ["python", "simulator.py", "--server", "--host", "0.0.0.0", "--port", "8000"]