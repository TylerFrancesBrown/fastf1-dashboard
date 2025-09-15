import React, { useState, useEffect } from "react";
import RaceResultsTable from "./components/race-results-table";
import YearDropdown from "./components/year-dropdown";
import RaceDropdown from "./components/race-dropdown";


function App() {
  const [years, setYears] = useState<number[]>([]);
  const [races, setRaces] = useState<{ full_name: string; short_name: string }[]>([]);
  const [year, setYear] = useState<number | null>(null);
  const [race, setRace] = useState<string>("");

  // Fetch years on load
  useEffect(() => {
    fetch("http://127.0.0.1:5000/years")
      .then(res => res.json())
      .then(data => {
        setYears(data.years);
        if (data.years.length > 0) {
          setYear(data.years[0]); // default latest year
        }
      });
  }, []);

  // Fetch races when year changes
  useEffect(() => {
    if (year !== null) {
      fetch(`http://127.0.0.1:5000/races?year=${year}`)
        .then((res) => res.json())
        .then((data) => {
          setRaces(data.races); // now array of {full_name, short_name}
          setRace(""); 
        });
    }
  }, [year]);



  return (
    <div className="p-6">
      <YearDropdown years={years} selectedYear={year} onChange={setYear} />
      <RaceDropdown races={races} selectedRace={race} onChange={setRace} />

      <h1 className="text-2xl font-bold mb-4 mt-4">
        {race} {year} Results
      </h1>

      {year && race && <RaceResultsTable year={year} race={race} />}
    </div>
  );
}

export default App;
