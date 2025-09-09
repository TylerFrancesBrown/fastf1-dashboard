def format_race_result(results):
    return {
        "results": [
            {
                "driver_number": row["driver_number"],
                "driver_name": row["driver_name"],
                "team_name": row["team_name"],
                "position": row["position"],
                "laps": row["laps"],
                "time_or_status": row["time_or_status"],
                "points": row["points"]
            }
            for row in results
        ]
    }

def convert_timeDelta(timedelta):
    seconds = timedelta.total_seconds()
    minutes = divmod(seconds, 60)
    return f"{int(minutes[0])}:{minutes[1]:.3f}"