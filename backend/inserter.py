import math
import datetime

def convert_timeDelta(timedelta_obj):
    """
    Convert a timedelta object to a string.
    - If under 1 hour: "MM:SS.mmm"
    - If 1 hour or more: "H:MM:SS.mmm"
    """
    total_seconds = int(timedelta_obj.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(timedelta_obj.microseconds / 1000)

    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}.{milliseconds:03}"  # H:MM:SS.mmm
    else:
        return f"{minutes}:{seconds:02}.{milliseconds:03}"  # MM:SS.mmm

def insert_results(conn, year, grand_prix, results):
    """
    Insert race results into the database.
    Handles finished times, DNFs/DNS/DSQ, NaN, and unexpected FastF1 values.
    """
    cur = conn.cursor()

    # Insert race row
    cur.execute("""
        INSERT INTO races (year, grand_prix)
        VALUES (%s, %s)
        ON CONFLICT (year, grand_prix) DO UPDATE SET grand_prix=EXCLUDED.grand_prix
        RETURNING race_id;
    """, (year, grand_prix))
    race_id = cur.fetchone()[0]

    for _, row in results.iterrows():
        # Insert or get driver
        cur.execute("""
            INSERT INTO drivers (driver_number, code, first_name, last_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (code) DO UPDATE SET driver_number=EXCLUDED.driver_number
            RETURNING driver_id;
        """, (int(row['DriverNumber']), row['Abbreviation'], row['FirstName'], row['LastName']))
        driver_id = cur.fetchone()[0]

        # Insert or get team
        cur.execute("""
            INSERT INTO teams (name)
            VALUES (%s)
            ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name
            RETURNING team_id;
        """, (row['TeamName'],))
        team_id = cur.fetchone()[0]

        # Handle time_or_status safely
        race_time = row.get('Time', None)
        status = row['Status']

        if isinstance(race_time, datetime.timedelta):
            # Finished: convert timedelta to smart string
            time_or_status = convert_timeDelta(race_time)
        elif isinstance(race_time, float) and math.isnan(race_time):
            # NaN → DNF/DNS/DSQ
            time_or_status = status if status in ['DNF', 'DNS', 'DSQ'] else 'DNF'
        elif isinstance(race_time, str):
            # Weird string value → normalize
            time_or_status = status if status in ['DNF', 'DNS', 'DSQ'] else 'DNF'
        else:
            # Catch-all fallback
            time_or_status = 'DNF'

        # Insert race result
        cur.execute("""
            INSERT INTO race_results (race_id, driver_id, team_id, position, laps, time_or_status, points)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (race_id, driver_id) DO UPDATE 
            SET position=EXCLUDED.position, laps=EXCLUDED.laps, 
                time_or_status=EXCLUDED.time_or_status, points=EXCLUDED.points;
        """, (race_id, driver_id, team_id,
              int(row['Position']), int(row['Laps']),
              time_or_status, float(row['Points'])))

    conn.commit()
