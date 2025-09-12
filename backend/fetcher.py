from db import get_db_connection
from fastf1_utils import get_race_results
from inserter import insert_results

def fetch_race_results_from_db(year, grand_prix):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Get race_id
            cur.execute("""
                SELECT race_id
                FROM races
                WHERE year = %s AND full_name = %s
                LIMIT 1;
            """, (year, grand_prix))
            result = cur.fetchone()
            if not result:
                return []  # no race found
            race_id = result[0]

        with conn.cursor() as cur:
            # Check if results exist
            cur.execute("""
                SELECT COUNT(*) 
                FROM race_results
                WHERE race_id = %s;
            """, (race_id,))
            count = cur.fetchone()[0]

        if count == 0:
            # Fetch from FastF1 and insert
            results_to_insert = get_race_results(year, grand_prix)  # your FastF1 helper
            insert_results(conn, year, grand_prix, results_to_insert)

        # Fetch final results
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    rr.position,
                    rr.laps,
                    rr.time_or_status,
                    rr.points,
                    rr.driver_number,
                    d.driver_id,
                    d.first_name,
                    d.last_name,
                    d.code,
                    rr.team_name
                FROM race_results rr
                JOIN drivers d ON rr.driver_id = d.driver_id
                WHERE rr.race_id = %s
                ORDER BY rr.position;
            """, (race_id,))
            rows = cur.fetchall()

        return [
            {
                "position": row[0],
                "laps": row[1],
                "time_or_status": row[2],
                "points": row[3],
                "driver_number": row[4],
                "driver_id": row[5],
                "first_name": row[6],
                "last_name": row[7],
                "code": row[8],
                "team_name": row[9]
            }
            for row in rows
        ]
    finally:
        conn.close()



def fetch_available_years():
    conn = get_db_connection()  # connection opened here

    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT year FROM races ORDER BY year DESC;")
        years = [row[0] for row in cur.fetchall()]
    return {"years": years}

def fetch_races_in_year(year,):
    conn = get_db_connection()  # connection opened here

    with conn.cursor() as cur:
        cur.execute("SELECT full_name FROM races WHERE year = %s AND round_num <> 0 ORDER BY round_num;", (year,))
        races = [row[0] for row in cur.fetchall()]
    return {"races": races}
