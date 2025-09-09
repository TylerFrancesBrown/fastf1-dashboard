import fastf1

def get_race_results(year, grand_prix):
    session = fastf1.get_session(year, grand_prix, 'R')  # Race
    session.load()

    # Include 'Time' column instead of 'RaceTime'
    results = session.results[['Abbreviation', 'DriverNumber', 'FirstName', 'LastName',
                               'TeamName', 'Position', 'Laps', 'Status', 'Points', 'Time']]

    # Convert Time (timedelta) to string if it exists
    results['Time'] = results['Time'].apply(lambda x: str(x) if x is not None else None)

    return results
