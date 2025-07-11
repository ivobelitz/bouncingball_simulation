from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import pandas as pd
import io
import plotly.graph_objs as go
import plotly.utils
import json
import os


def load_config():
    """Load configuration from config.json file"""
    config_path = os.path.join(os.path.dirname(__file__), 'dashboard.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Warning: Configuration not found at {config_path}. Using default settings.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Warning: Error parsing configuration {e}. Using default settings.")
        return {}

# Load configuration
config = load_config()


app = Flask(__name__)
CORS(app)

# API server URL - use environment variable or fallback to localhost
API_URL = os.getenv("SIMULATOR_URL", "http://localhost:8000")

# Hardcoded planet gravity values (fallback if API is unavailable)
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


@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html', planets=list(PLANETS.keys()))

user_input_endpoint = config['user_input']['endpoint']
@app.route(user_input_endpoint, methods=['POST'])
def simulate():
    """Run simulation and return plot data"""
    try:
        data = request.get_json()
        planet = data.get('planet')
        height = float(data.get('height'))
        
        if height <= 0:
            return jsonify({'error': 'Height must be greater than 0'}), 400
        
        # Make API request to simulation server
        payload = {
            "planet": planet,
            "height": height
        }

        address = config['simulation_request']['address']
        port = config['simulation_request']['port']
        endpoint = config['simulation_request']['endpoint']
        print("URL: ", f"{address}:{port}{endpoint}")
            
        response = requests.post(f"{address}:{port}{endpoint}", json=payload, timeout=30)
        response.raise_for_status()
        
        # Parse CSV data
        df = pd.read_csv(io.StringIO(response.text))
        
        # Create Plotly graph
        fig = go.Figure()
        
        # Convert data to lists to ensure proper JSON serialization
        time_data = df['time'].tolist()
        height_data = df['h'].tolist()
        
        # Add trajectory line
        fig.add_trace(go.Scatter(
            x=time_data,
            y=height_data,
            mode='lines+markers',
            name='Ball Height',
            line=dict(color='blue', width=2),
            marker=dict(size=2)
        ))
        
        # Add ground line
        fig.add_trace(go.Scatter(
            x=[time_data[0], time_data[-1]],
            y=[0, 0],
            mode='lines',
            name='Ground',
            line=dict(color='brown', width=3),
            showlegend=False
        ))
        
        # Customize layout
        gravity = PLANETS.get(planet, 9.81)
        fig.update_layout(
            title=f'Ball Trajectory on {planet} (Drop Height: {height}m, g={gravity}m/s²)',
            xaxis_title='Time (s)',
            yaxis_title='Height (m)',
            template='plotly_white',
            showlegend=True,
            height=500,
            yaxis=dict(range=[0, max(height_data) * 1.1])
        )
        
        # Convert to JSON
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({
            'success': True,
            'graph': graph_json,
            'message': f'Simulation completed for {planet}'
        })
        
    except ValueError as e:
        return jsonify({'error': 'Please enter a valid number for height'}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Simulation server error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/api/planets', methods=['GET'])
def get_planets():
    """Get available planets and their gravity values"""
    try:
        # Try to get planets from simulation server
        response = requests.get(f"{API_URL}/planets", timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    # Fallback to hardcoded values
    return jsonify(PLANETS)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)