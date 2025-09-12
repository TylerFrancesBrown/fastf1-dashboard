import fastf1
import unicodedata



def get_race_results(year, grand_prix):
    session = fastf1.get_session(year, grand_prix, 'R')  # Race
    session.load()

    # Keep Time as timedelta
    results = session.results[['Abbreviation', 'DriverNumber', 'FirstName', 'LastName',
                               'TeamName', 'Position', 'Laps', 'Status', 'Points', 'Time']]

    return results

def convert_timeDelta(timedelta):
    seconds = timedelta.total_seconds()
    minutes = divmod(seconds, 60)
    return f"{int(minutes[0])}:{minutes[1]:.3f}"

def normalize_driver_id(first_name, last_name):
    """
    Returns a normalized driver_id in the format firstname_lastname.
    """

    # Remove accents
    last_name = ''.join(c for c in unicodedata.normalize('NFKD', last_name) if not unicodedata.combining(c))
    first_name = ''.join(c for c in unicodedata.normalize('NFKD', first_name) if not unicodedata.combining(c))
    
    # Lowercase and replace spaces with underscores
    return f"{first_name.lower()}_{last_name.lower().replace(' ', '_')}"