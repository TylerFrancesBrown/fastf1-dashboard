from db import get_connection

def insert_results(year, grand_prix, results):
    conn = get_connection()
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

        # Determine time_or_status
        race_time = row.get('Time', None)
        status = row['Status']

        if race_time is not None:
            time_or_status = race_time  # actual race completion time
        else:
            time_or_status = status  # DNF, DNS, Power Unit, Fuel pressure, etc.



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
    cur.close()
    conn.close()
