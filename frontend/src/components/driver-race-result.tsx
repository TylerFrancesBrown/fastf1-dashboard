import React from "react";
import type { RaceResult } from "../types";

interface Props {
  result: RaceResult;
}

const DriverRaceResultRow: React.FC<Props> = ({ result }) => {
  return (
    <tr className="hover:bg-gray-100">
      <td className="px-4 py-2 text-center">{result.position}</td>
      <td className="px-4 py-2 text-center">{result.driver_number}</td>
      <td className="px-4 py-2">{result.driver_name}</td>
      <td className="px-4 py-2">{result.team_name}</td>
      <td className="px-4 py-2 text-center">{result.laps}</td>
      <td className="px-4 py-2 text-right">{result.time_or_status}</td>
      <td className="px-4 py-2 text-center">{result.points}</td>
    </tr>
  );
};

export default DriverRaceResultRow;
