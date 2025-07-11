# Bouncing Ball Simulation System

This system simulates a bouncing ball using FMU (Functional Mock-up Unit) with different planetary gravity settings.

## Components

### 1. Dashboard (`dashboard/dashboard.py`)
- Web-based dashboard built with Flask and Plotly
- Interactive planet selection with gravity values
- Height input field for drop height
- Real-time plotting of simulation results
- Communicates with simulator via HTTP API

### 2. FMU Simulator (`simulator/simulator.py`)
- Uses FMPy library to run bouncing ball FMU
- Flask web server with CORS support for HTTP API
- Accepts parameters for height and planet selection
- Returns CSV data with time, height, and velocity information

## Quick Start with Deployment Manager

1. **Copy deployment files:**
   - Copy the `Dockerfiles` and the configuration JSON files to their corresponding directories
   - Copy the `docker-compose.yml` file to the root of the project

2. **Start the deployment:**
   - Run the setup script to build and start the Docker containers:
   ```bash
   ./setup_deployment.sh
   ```

3. **Access the dashboard:**
   - Open your web browser and go to: `http://localhost:5050`
   - The dashboard will automatically connect to the simulator service


## Docker Services

The Docker Compose configuration includes:

- **Simulator Service**: Runs on port 8000 (internal communication)
- **Dashboard Service**: Runs on port 5050 (accessible from host browser)
- **Shared Network**: Both services communicate via the `bouncingball_network`
- **Volume Mounting**: Simulator output is saved to `./simulator/output/`
  
## Troubleshooting

- **Services won't start**: Ensure Docker and Docker Compose are installed and running
- **Port conflicts**: If ports 5050 or 8000 are in use, modify the ports in docker-compose.yml
- **Dashboard can't reach simulator**: Check that both services are running and on the same Docker network
- **"FMU file not found" error**: Verify `bouncingBall.fmu` is present in the simulator directory