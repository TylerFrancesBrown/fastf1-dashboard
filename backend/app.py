from flask import Flask, request, jsonify
from flask_cors import CORS
import fastf1
import pandas as pd
from pathlib import Path
from utils import format_race_result
from fetcher import *

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
    results = fetch_race_results_from_db(year, race)
    return jsonify(format_race_result(results))

@app.get("/years")
def get_years():
    return jsonify(fetch_available_years())

@app.get("/races")
def get_races():
    year = request.args.get('year', type=int)
    return jsonify(fetch_races_in_year(year))



if __name__ == "__main__":
    app.run(debug=True)