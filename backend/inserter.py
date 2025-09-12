import datetime
import math
import fastf1
from utils import *
from fastf1_utils import normalize_driver_id, convert_timeDelta  # your helper functions

def convert_timeDelta(td: datetime.timedelta) -> str:
    """Convert timedelta to string like '1:32.123'"""
    total_seconds = td.total_seconds()
    minutes, seconds = divmod(total_seconds, 60)
    seconds, milliseconds = divmod(seconds, 1)
    return f"{int(minutes)}:{int(seconds):02d}.{int(milliseconds*1000):03d}"

def insert_results(conn, year, grand_prix, results):
    """
    Insert race results into the database.
    Handles finished times, DNFs/DNS/DSQ, NaN, and unexpected FastF1 values.
    Stores driver numbers directly in race_results.
    """
    cur = conn.cursor()

    # Compute race_id
    race_id = f"{year}-{grand_prix.replace(' ', '')}"

    # Check if race exists
    cur.execute("SELECT round_num FROM races WHERE race_id = %s", (race_id,))
    existing = cur.fetchone()
    if not existing:
        # If race info missing, insert all races for the year
        insert_all_races_for_year(conn, year)

    for _, row in results.iterrows():
        driver_id = normalize_driver_id(row['FirstName'], row['LastName'])

        # Insert or update driver
        cur.execute("""
            INSERT INTO drivers (driver_id, first_name, last_name, code)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (driver_id) DO UPDATE
            SET first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                code = EXCLUDED.code;
        """, (driver_id, row['FirstName'], row['LastName'], row['Abbreviation']))

        # Ensure team exists (no fetchone needed)
        cur.execute("""
            INSERT INTO teams (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
        """, (row['TeamName'],))
        team_name = row['TeamName']

        # Handle race time / status safely
        race_time = row.get('Time', None)
        status = row['Status']

        if isinstance(race_time, datetime.timedelta):
            time_or_status = convert_timeDelta(race_time)
        elif isinstance(race_time, float) and math.isnan(race_time):
            time_or_status = status if status in ['DNF', 'DNS', 'DSQ'] else 'DNF'
        elif isinstance(race_time, str):
            time_or_status = status if status in ['DNF', 'DNS', 'DSQ'] else 'DNF'
        else:
            time_or_status = 'DNF'

        # Insert/update race result including driver_number
        driver_number = row.get('DriverNumber')  # may be None if missing
        cur.execute("""
            INSERT INTO race_results (race_id, driver_id, team_name, position, laps, time_or_status, points, driver_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (race_id, driver_id) DO UPDATE
            SET position = EXCLUDED.position,
                laps = EXCLUDED.laps,
                time_or_status = EXCLUDED.time_or_status,
                points = EXCLUDED.points,
                driver_number = EXCLUDED.driver_number,
                team_name = EXCLUDED.team_name;
        """, (race_id, driver_id, team_name,
              int(row['Position']), int(row['Laps']),
              time_or_status, float(row['Points']), driver_number))

    conn.commit()
    cur.close()
    print(f"✅ Results for {grand_prix} {year} inserted/updated successfully!")


def insert_all_races_for_year(conn, year):
    """
    Fetch all races for a given year using FastF1 and insert into the races table.
    """
    cur = conn.cursor()

    schedule = fastf1.get_event_schedule(year)
    
    for _, race in schedule.iterrows():
        round_num = race['RoundNumber']
        full_name = race['EventName']
        
        # Always remove spaces for consistency
        race_id = f"{year}-{full_name.replace(' ', '')}"

        cur.execute("""
            INSERT INTO races (race_id, year, round_num, full_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (race_id) DO UPDATE
            SET round_num = EXCLUDED.round_num,
                full_name = EXCLUDED.full_name
        """, (race_id, year, round_num, full_name))

    conn.commit()
    cur.close()
    print(f"✅ All races for {year} inserted/updated successfully!")
