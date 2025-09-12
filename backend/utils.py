def format_race_result(results):
    return {
        "results": [
            {
                "driver_number": row["driver_number"],
                "driver_name": f"{row['first_name']} {row['last_name']}",
                "team_name": row["team_name"],
                "position": row["position"],
                "laps": row["laps"],
                "time_or_status": row["time_or_status"],
                "points": row["points"]
            }
            for row in results
        ]
    }
