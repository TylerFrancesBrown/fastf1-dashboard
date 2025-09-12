import fastf1
from db import get_db_connection
from inserter import insert_results  # your function
import pandas as pd
from fetcher import *

if __name__ == "__main__":
    conn = get_db_connection()
    races_dict = fetch_races_in_year(2022)
    for race in races_dict["races"]:
        grand_prix = race

        # Fetch results from FastF1
        session = fastf1.get_session(2022, grand_prix, 'R')
        session.load()
        results = session.results

        # Insert into your database
        insert_results(conn, 2022, grand_prix, results)
        print(f"✅ {grand_prix} {2022} results inserted!")
    conn.close()
    print(f"✅ All results inserted!")