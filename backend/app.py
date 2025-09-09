from flask import Flask, request, jsonify
from flask_cors import CORS
import fastf1
import pandas as pd
from pathlib import Path
from utils import format_race_result
from db import get_race_results_from_db

# -----------------------------
# Your existing functions
# -----------------------------


# -----------------------------
# Flask setup
# -----------------------------
Path("cache").mkdir(exist_ok=True)
fastf1.Cache.enable_cache("cache")

app = Flask(__name__)
CORS(app)

@app.route('/race-results')
def race_results():
    year = request.args.get('year', type=int)
    race = request.args.get('race', type=str)
    results = get_race_results_from_db(year, race)
    return jsonify(format_race_result(results))


if __name__ == "__main__":
    app.run(debug=True)