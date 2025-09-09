import psycopg2
from fastf1_utils import get_race_results
from inserter import insert_results

def get_db_connection():
    return psycopg2.connect(
        dbname="f1db",
        user="postgres",
        password="Harpswell2017!",
        host="localhost",
        port="5432"
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
        driver_id SERIAL PRIMARY KEY,
        driver_number INT NOT NULL,
        code VARCHAR(5) UNIQUE,
        first_name VARCHAR(50),
        last_name VARCHAR(50)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        team_id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS races (
        race_id SERIAL PRIMARY KEY,
        year INT NOT NULL,
        grand_prix VARCHAR(100) NOT NULL,
        UNIQUE(year, grand_prix)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS race_results (
        result_id SERIAL PRIMARY KEY,
        race_id INT REFERENCES races(race_id) ON DELETE CASCADE,
        driver_id INT REFERENCES drivers(driver_id),
        team_id INT REFERENCES teams(team_id),
        position INT,
        laps INT,
        time_or_status VARCHAR(50),
        points FLOAT,
        UNIQUE(race_id, driver_id)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

def get_race_results_from_db(year, grand_prix):
    conn = get_db_connection()  # connection opened here
    try:
        with conn.cursor() as cur:
            # Check if results exist
            cur.execute("""
                SELECT COUNT(*) AS count
                FROM race_results rr
                JOIN races r ON rr.race_id = r.race_id
                WHERE r.year = %s AND r.grand_prix = %s
            """, (year, grand_prix))
            count = cur.fetchone()[0]

        # If no results, fetch from API and insert
        if count == 0:
            results_to_insert = get_race_results(year, grand_prix)
            insert_results(conn, year, grand_prix, results_to_insert)

        # Fetch final results
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    d.driver_number,
                    d.first_name || ' ' || d.last_name AS driver_name,
                    t.name AS team_name,
                    rr.position,
                    rr.laps,
                    rr.time_or_status,
                    rr.points
                FROM race_results rr
                JOIN races r ON rr.race_id = r.race_id
                JOIN drivers d ON rr.driver_id = d.driver_id
                JOIN teams t ON rr.team_id = t.team_id
                WHERE r.year = %s AND r.grand_prix = %s
                ORDER BY rr.position
            """, (year, grand_prix))
            rows = cur.fetchall()

        # Format results as list of dicts
        return [
            {
                "driver_number": row[0],
                "driver_name": row[1],
                "team_name": row[2],
                "position": row[3],
                "laps": row[4],
                "time_or_status": row[5],
                "points": row[6]
            }
            for row in rows
        ]
    finally:
        conn.close()  # connection closed here