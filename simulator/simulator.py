from fmpy import *
from fmpy.util import plot_result
import numpy as np
import pandas as pd
import sys
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import tempfile
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Planet gravity values
PLANETS = {
    "Earth": 9.81,
    "Moon": 1.62,
    "Mars": 3.71,
    "Jupiter": 24.79,
    "Venus": 8.87,
    "Mercury": 3.7,
    "Saturn": 10.44,
    "Uranus": 8.69,
    "Neptune": 11.15
}

@app.route('/planets', methods=['GET'])
def get_planets():
    """Get available planets and their gravity values"""
    return jsonify(PLANETS)

@app.route('/simulate', methods=['POST'])
def simulate_endpoint():
    """Run simulation via HTTP request"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        planet = data.get('planet', 'Earth')
        height = data.get('height', 3.0)
        
        # Validate inputs
        if planet not in PLANETS:
            return jsonify({"error": f"Unknown planet: {planet}"}), 400
        
        if not isinstance(height, (int, float)) or height <= 0:
            return jsonify({"error": "Height must be a positive number"}), 400
        
        gravity = PLANETS[planet]
        logger.info(f"Running simulation for {planet} with height {height}m and gravity {gravity}m/s²")
        
        # Run simulation
        csv_content = simulate_fmu_and_return_csv(height, gravity, planet)
        
        # Return CSV content as response
        return csv_content, 200, {'Content-Type': 'text/csv'}
        
    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

def simulate_fmu_and_return_csv(height=3.0, gravity=9.81, planet="Earth"):
    """
    Simulate the bouncing ball FMU with given parameters and return CSV content
    
    Args:
        height (float): Initial drop height in meters
        gravity (float): Gravity acceleration in m/s² (positive value)
        planet (str): Name of the planet for reference
    
    Returns:
        str: CSV content as string
    """
    try:
        fmu = 'bouncingBall.fmu'
        
        # Check if FMU file exists
        if not os.path.exists(fmu):
            raise FileNotFoundError(f"FMU file not found: {fmu}")
        
        dump(fmu)
        
        # Set up simulation parameters
        start_values = {
            'h': height,  # initial height
            'g': -abs(gravity)  # gravity should be negative for downward acceleration
        }
        
        # Run simulation
        result = simulate_fmu(
            filename=fmu, 
            start_values=start_values, 
            stop_time=10.0, 
            output_interval=0.01
        )
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'time': result['time'],
            'h': result['h'],
            'v': result['v']
        })
        
        # Convert to CSV string
        csv_content = results_df.to_csv(index=False)
        
        logger.info(f"Simulation completed successfully for {planet}")
        logger.info(f"Initial height: {height}m, Gravity: {gravity}m/s²")
        
        return csv_content
        
    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}")
        raise e

if __name__ == '__main__':
    logger.info("Starting bouncing ball simulator web server on port 8000")
    app.run(host='0.0.0.0', port=8000, debug=False)