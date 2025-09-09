import React, { useEffect, useState } from "react";
import DriverRaceResultRow from "./driver-race-result";
import type { RaceResult } from "../types";

export default function RaceResultsTable() {
  const [data, setData] = useState<RaceResult[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/race-results?year=2025&race=Japan")
      .then((res) => res.json())
      .then((data) => {
        console.log("Fetched data:", data);
        // if backend returns {results: [...]}, unwrap it
        setData(Array.isArray(data) ? data : data.results);
      })
      .catch((err) => console.error("Error fetching results:", err));
  }, []);

  return (
    <table className="table-auto border-collapse border border-gray-300 w-full">
      <thead>
        <tr>
          <th className="px-4 py-2">POS</th>
          <th className="px-4 py-2">NO.</th>
          <th className="px-4 py-2">DRIVER</th>
          <th className="px-4 py-2">TEAM</th>
          <th className="px-4 py-2">LAPS</th>
          <th className="px-4 py-2">TIME / RETIRED</th>
          <th className="px-4 py-2">PTS.</th>
        </tr>
      </thead>
      <tbody>
        {data.map((result, idx) => (
          <DriverRaceResultRow key={idx} result={result} />
        ))}
      </tbody>
    </table>
  );
}
