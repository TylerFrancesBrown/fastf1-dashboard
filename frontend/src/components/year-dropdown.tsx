import React from "react";

interface YearDropdownProps {
  years: number[];
  selectedYear: number | null;
  onChange: (year: number) => void;
}

const YearDropdown: React.FC<YearDropdownProps> = ({ years, selectedYear, onChange }) => {
  return (
    <div className="inline-block mr-4">
      <label className="mr-2 font-semibold">Year:</label>
      <select
        value={selectedYear ?? ""}
        onChange={(e) => onChange(Number(e.target.value))}
        className="border p-2"
      >
        {years.map((y) => (
          <option key={y} value={y}>
            {y}
          </option>
        ))}
      </select>
    </div>
  );
};

export default YearDropdown;