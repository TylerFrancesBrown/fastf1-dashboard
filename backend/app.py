from flask import Flask, request, jsonify
from flask_cors import CORS
import fastf1
import pandas as pd
from pathlib import Path

# -----------------------------
# Your existing functions
# -----------------------------

def get_all_fastest_laps(session):
    """Return a DataFrame with each driver's fastest lap from the session."""
    fastest_laps = []

    for driver_id in session.drivers:
        lap = session.laps.pick_drivers(driver_id).pick_fastest()
        lap_df = pd.DataFrame([lap])
        fastest_laps.append(lap_df)

    fastest_laps_df = pd.concat(fastest_laps, ignore_index=True)
    fastest_laps_df['LapTime'] = fastest_laps_df['LapTime'].apply(convert_timeDelta)
    return fastest_laps_df

def convert_timeDelta(timedelta):
    seconds = timedelta.total_seconds()
    minutes = divmod(seconds, 60)
    return f"{int(minutes[0])}:{minutes[1]:.3f}"

def format_leaderboard(df):
    """Return a list of dicts for JSON response"""
    leaderboard = []
    for pos, row in enumerate(df.itertuples(), 1):
        leaderboard.append({
            "Position": pos,
            "Driver": row.Driver,
            "LapTime": row.LapTime
        })
    return leaderboard

# -----------------------------
# Flask setup
# -----------------------------
Path("cache").mkdir(exist_ok=True)
fastf1.Cache.enable_cache("cache")

app = Flask(__name__)
CORS(app)

@app.route("/fastest-lap")
def fastest_lap():
    """Return only the single fastest lap"""
    session = fastf1.get_session(2023, "Bahrain", "Q")
    session.load()
    fastest = session.laps.pick_fastest()
    return jsonify({
        "Driver": fastest["Driver"],
        "LapTime": str(fastest["LapTime"])
    })

@app.route("/leaderboard")
def leaderboard():
    """Return leaderboard for any session. Defaults to latest session."""
    # Query parameters
    year = request.args.get("year")
    gp = request.args.get("gp")
    session_type = request.args.get("session")  # 'Q', 'R', 'FP1', etc.

    # If any parameter is missing, find the most recent session
    if not year or not gp or not session_type:
        schedule = fastf1.get_event_schedule(2023, include_testing=False)
        # Filter only past events
        past_events = schedule[schedule['EventDate'] <= fastf1.datetime.datetime.utcnow()]
        last_event = past_events.iloc[-1]  # Most recent
        year = last_event['Year']
        gp = last_event['EventName']
        session_type = 'Q'  # Default to qualifying for the latest event

    # Make sure year is int
    year = int(year)

    # Load session
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    df = get_all_fastest_laps(session)

    return jsonify(format_leaderboard(df))

if __name__ == "__main__":
    app.run(debug=True)