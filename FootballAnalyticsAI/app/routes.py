import sys
import os
from flask import Flask, render_template, jsonify
import pandas as pd
import json

app = Flask(__name__)

# --- Configuration: Hardcoded File Paths ---
# Get the absolute path to the 'dataset/processed' directory
# This assumes 'routes.py' is in 'app' and 'data' is a sibling of 'app'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed'))
CSV_PATH = os.path.join(BASE_DIR, 'matches_data.csv')
JSON_PATH = os.path.join(BASE_DIR, 'tactical_report.json')

# --- Cache Busting ---
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache-bust.
    """
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# --- Helper Functions ---
def load_tactical_data(json_path):
    """Helper to ensure tactical data is always in a valid format."""
    if not os.path.exists(json_path):
        return [{"tactical_observation": "Match engine initializing. Waiting for live feed..."}]
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]
    except (json.JSONDecodeError, IOError):
        return [{"tactical_observation": "Error reading or parsing tactical data."}]

def safe_get(metrics_dict, key, default=0):
    """Safely get a value from metrics dictionary with default fallback."""
    try:
        value = metrics_dict.get(key, default)
        if pd.isna(value) or value is None:
            return default
        # Attempt to convert to float, return default if it fails
        return float(value)
    except (TypeError, ValueError):
        return default

def get_default_match_metrics():
    """Return default match metrics for demonstration/initialization."""
    return {
        'home_team': 'Arsenal', 'away_team': 'Chelsea',
        'home_score': 0, 'away_score': 0, 'match_time': '00:00',
        'possession': 50, 'home_xG': 0.0, 'away_xG': 0.0,
        'attacking': 50, 'defensive': 50, 'speed': 50, 'discipline': 50,
        'shots_on_target': 0, 'saves': 0, 'corners': 0, 'fouls': 0
    }

# --- Main App Routes ---
@app.route('/')
def index():
    """Renders the main dashboard, loading initial data directly."""
    # 1. Load Match Stats
    match_metrics = get_default_match_metrics()
    if os.path.exists(CSV_PATH):
        try:
            matches_df = pd.read_csv(CSV_PATH)
            if not matches_df.empty:
                match_metrics.update(matches_df.iloc[0].to_dict())
        except Exception as e:
            print(f"Initial CSV Load Error: {e}")

    # 2. Load Tactical Insights
    tactical_report = load_tactical_data(JSON_PATH)

    # 3. Render Template
    return render_template('index.html', 
                           tactical_report=tactical_report,
                           match_metrics=match_metrics)

# --- API Endpoints ---
@app.route('/api/insight')
def api_insight():
    """API endpoint for the live AI tactical insight."""
    report = load_tactical_data(JSON_PATH)
    insight = report[0].get('tactical_observation', 'Analyzing match data...')
    return jsonify({"insight": insight})

@app.route('/api/match-data')
def api_match_data():
    """API endpoint for live chart and metric updates."""
    if os.path.exists(CSV_PATH):
        try:
            matches_df = pd.read_csv(CSV_PATH)
            if not matches_df.empty:
                metrics = matches_df.iloc[0].to_dict()
                # Ensure all fields are present for the frontend
                return jsonify({
                    'home_team': metrics.get('home_team', 'N/A'),
                    'away_team': metrics.get('away_team', 'N/A'),
                    'home_score': safe_get(metrics, 'home_score'),
                    'away_score': safe_get(metrics, 'away_score'),
                    'match_time': metrics.get('match_time', '00:00'),
                    'possession': safe_get(metrics, 'possession', 50),
                    'home_xG': safe_get(metrics, 'home_xG', 0.0),
                    'away_xG': safe_get(metrics, 'away_xG', 0.0),
                    'attacking': safe_get(metrics, 'attacking', 50),
                    'defensive': safe_get(metrics, 'defensive', 50),
                    'speed': safe_get(metrics, 'speed', 50),
                    'discipline': safe_get(metrics, 'discipline', 50),
                })
        except Exception as e:
            print(f"API Match Data Error: {e}")
    
    # Fallback to default metrics if file doesn't exist or fails to load
    return jsonify(get_default_match_metrics())

# --- Static Page Routes (unchanged) ---
@app.route('/matches')
def matches():
    return render_template('matches.html')

@app.route('/strategy')
def strategy():
    return render_template('strategy.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)