from db import init_db
from fastf1_utils import get_race_results
from inserter import insert_results

if __name__ == "__main__":
    init_db()

    results = get_race_results(2022, "Bahrain")
    insert_results(2022, "Bahrain", results)

    print("✅ 2022 Bahrain GP results inserted into DB!")
