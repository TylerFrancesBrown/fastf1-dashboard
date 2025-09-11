import React, { useState } from "react";
import RaceResultsTable from "./components/race-results-table";

function App() {
  const [year, setYear] = useState(2025);
  const [race, setRace] = useState("Monza");

  const handleYearChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setYear(Number(event.target.value));
  };

  const handleRaceChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setRace(event.target.value);
  };

  return (
    <div className="p-6">
      {/* Year Dropdown */}
      <label className="mr-2 font-semibold">Year:</label>
      <select
        value={year}
        onChange={handleYearChange}
        className="border p-2 mr-4"
      >
        <option value={2023}>2023</option>
        <option value={2024}>2024</option>
        <option value={2025}>2025</option>
      </select>

      {/* Race Dropdown */}
      <label className="mr-2 font-semibold">Race:</label>
      <select
        value={race}
        onChange={handleRaceChange}
        className="border p-2"
      >
        <option value="Monza">Monza</option>
        <option value="Silverstone">Silverstone</option>
        <option value="Spa">Spa</option>
        <option value="Monaco">Monaco</option>
      </select>

      <h1 className="text-2xl font-bold mb-4 mt-4">
        {race} GP {year} Results
      </h1>

      {/* Automatically re-fetches when year or race changes */}
      <RaceResultsTable year={year} race={race} />
    </div>
  );
}

export default App;
