import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="f1db",
        user="postgres",
        password="Harpswell2017!",
        host="localhost",
        port="5432"
    )

def init_db():
    conn = get_connection()
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
