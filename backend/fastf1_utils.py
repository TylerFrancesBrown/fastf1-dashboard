import fastf1

def get_race_results(year, grand_prix):
    session = fastf1.get_session(year, grand_prix, 'R')  # Race
    session.load()

    # Keep Time as timedelta
    results = session.results[['Abbreviation', 'DriverNumber', 'FirstName', 'LastName',
                               'TeamName', 'Position', 'Laps', 'Status', 'Points', 'Time']]

    return results
