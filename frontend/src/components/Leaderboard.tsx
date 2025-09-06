import React, { useEffect, useState } from 'react';

type Lap = {
  Position: number;
  Driver: string;
  LapTime: string;
};

export default function Leaderboard() {
  const [laps, setLaps] = useState<Lap[]>([]);
  const [year, setYear] = useState<number | null>(null);
  const [gp, setGp] = useState<string>('');
  const [session, setSession] = useState<string>('Q'); // default to qualifying

  const fetchLeaderboard = async () => {
    try {
      // Construct query string only if parameters exist
      let url = 'http://127.0.0.1:5000/leaderboard';
      const params = new URLSearchParams();
      if (year) params.append('year', year.toString());
      if (gp) params.append('gp', gp);
      if (session) params.append('session', session);
      if ([...params].length > 0) url += '?' + params.toString();

      const res = await fetch(url);
      const data = await res.json();
      setLaps(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchLeaderboard();
  }, [year, gp, session]); // refetch if any parameter changes

  return (
    <div>
      <h2>Leaderboard</h2>

      {/* Optional filters */}
      <div>
        <input
          type="number"
          placeholder="Year"
          value={year ?? ''}
          onChange={e => setYear(Number(e.target.value) || null)}
        />
        <input
          type="text"
          placeholder="GP Name"
          value={gp}
          onChange={e => setGp(e.target.value)}
        />
        <select value={session} onChange={e => setSession(e.target.value)}>
          <option value="FP1">FP1</option>
          <option value="FP2">FP2</option>
          <option value="FP3">FP3</option>
          <option value="Q">Qualifying</option>
          <option value="R">Race</option>
        </select>
        <button onClick={fetchLeaderboard}>Fetch</button>
      </div>

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
