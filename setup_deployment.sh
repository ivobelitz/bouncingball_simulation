#!/bin/bash

# Script to set up and deploy the bouncing ball simulation

echo "Checking for required deployment files..."

# Check for dashboard.json
echo "Checking for dashboard.json..."
if [ ! -f "./dashboard/dashboard.json" ]; then
    echo "Error: dashboard.json not found in ./dashboard/dashboard.json"
    exit 1
fi

# Check for Dockerfile_dashboard
echo "Checking for Dockerfile_dashboard..."
if [ ! -f "./dashboard/Dockerfile_dashboard" ]; then
    echo "Error: Dockerfile_dashboard not found in ./dashboard/Dockerfile_dashboard"
    exit 1
fi

# Check for simulation_model.json
echo "Checking for simulation_model.json..."
if [ ! -f "./simulation_model/simulation_model.json" ]; then
    echo "Error: simulation_model.json not found in ./simulation_model/simulation_model.json"
    exit 1
fi

# Check for Dockerfile_simulation_model
echo "Checking for Dockerfile_simulation_model..."
if [ ! -f "./simulation_model/Dockerfile_simulation_model" ]; then
    echo "Error: Dockerfile_simulation_model not found in ./simulation_model/Dockerfile_simulation_model"
    exit 1
fi

# Check for docker-compose.yml
echo "Checking for docker-compose.yml..."
if [ ! -f "./docker-compose.yml" ]; then
    echo "Error: docker-compose.yml not found in current directory"
    exit 1
fi

# Build Docker images

echo "Building Dashboard image..."
docker build -t dashboard -f ./dashboard/Dockerfile_dashboard ./dashboard
if [ $? -ne 0 ]; then
    echo "Error: Failed to build Dashboard image"
    exit 1
fi

echo "Building Simulation Model image..."
docker build --platform linux/amd64 -t simulation_model -f ./simulation_model/Dockerfile_simulation_model ./simulation_model
if [ $? -ne 0 ]; then
    echo "Error: Failed to build Simulation Model image"
    exit 1
fi

# Start Docker Compose cluster
echo "Starting Docker Compose..."
docker compose up
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Docker Compose"
    exit 1
fi

echo "Deployment successful!"
