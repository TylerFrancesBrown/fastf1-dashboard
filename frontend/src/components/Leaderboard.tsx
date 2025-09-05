import React, { useEffect, useState } from 'react';

type Lap = {
  Position: number;
  Driver: string;
  LapTime: string;
};

export default function Leaderboard() {
  const [laps, setLaps] = useState<Lap[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/leaderboard')
      .then(res => res.json())
      .then(data => setLaps(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Leaderboard</h2>
      <table>
        <thead>
          <tr>
            <th>Pos</th>
            <th>Driver</th>
            <th>Lap Time</th>
          </tr>
        </thead>
        <tbody>
          {laps.map(lap => (
            <tr key={lap.Position}>
              <td>{lap.Position}</td>
              <td>{lap.Driver}</td>
              <td>{lap.LapTime}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}