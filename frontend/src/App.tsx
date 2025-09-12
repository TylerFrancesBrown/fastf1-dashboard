import React, { useState, useEffect } from "react";
import RaceResultsTable from "./components/race-results-table";

function App() {
  const [years, setYears] = useState<number[]>([]);
  const [races, setRaces] = useState<string[]>([]);
  const [year, setYear] = useState<number | null>(null);
  const [race, setRace] = useState<string>("");

  // Fetch years on load
  useEffect(() => {
    fetch("http://127.0.0.1:5000/years")
      .then(res => res.json())
      .then(data => {
        setYears(data.years);
        if (data.years.length > 0) {
          setYear(data.years[data.years.length - 1]); // default latest year
        }
      });
  }, []);

  // Fetch races when year changes
  useEffect(() => {
    fetch(`http://127.0.0.1:5000/races?year=${year}`)
      .then(res => res.json())
      .then(data => {
        setRaces(data.races);
        if (data.races.length > 0) {
          setRace(data.races[0]);
        }
      });
  }, [year]);

  return (
    <div className="p-6">
      {/* Year Dropdown */}
      <label className="mr-2 font-semibold">Year:</label>
      <select
        value={year ?? ""}
        onChange={(e) => setYear(Number(e.target.value))}
        className="border p-2 mr-4"
      >
        {years.map((y) => (
          <option key={y} value={y}>{y}</option>
        ))}
      </select>

      {/* Race Dropdown */}
      <label className="mr-2 font-semibold">Race:</label>
      <select
        value={race}
        onChange={(e) => setRace(e.target.value)}
        className="border p-2"
      >
        {races.map((r) => (
          <option key={r} value={r}>{r}</option>
        ))}
      </select>

      <h1 className="text-2xl font-bold mb-4 mt-4">
        {race} {year} Results
      </h1>

      {year && race && <RaceResultsTable year={year} race={race} />}
    </div>
  );
}

export default App;
