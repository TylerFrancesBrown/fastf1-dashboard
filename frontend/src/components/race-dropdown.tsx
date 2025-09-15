import React, { useEffect, useRef, useState } from "react";

interface Race {
  full_name: string;
  short_name: string;
}

interface RaceDropdownProps {
  races: Race[];
  selectedRace: string; // still storing full_name
  onChange: (race: string) => void;
}


const RaceDropdown: React.FC<RaceDropdownProps> = ({ races, selectedRace, onChange }) => {
  const [width, setWidth] = useState<number>(0);
  const spanRef = useRef<HTMLSpanElement>(null);

  useEffect(() => {
    if (spanRef.current) {
      setWidth(spanRef.current.scrollWidth + 25); 
    }
  }, [selectedRace]);

  return (
    <div className="inline-block mr-4">
      <span
        ref={spanRef}
        className="invisible absolute whitespace-nowrap text-sm font-bold px-3 py-1 border-2"
      >
        {selectedRace || "All"}
      </span>

      <select
        value={selectedRace}
        onChange={(e) => onChange(e.target.value)}
        className="
          px-3 py-1
          rounded-full
          text-sm font-bold
          border-2 border-white
          text-white
          bg-transparent
          outline-none
          cursor-pointer
        "
        style={{ width }}
      >
        <option value="" className="bg-black text-white font-bold">
          All
        </option>
        {races.map((r) => (
          <option
            key={r.full_name}
            value={r.full_name} // passed to fetcher
            className="bg-black text-white font-bold"
          >
            {r.short_name} {/* shown in dropdown */}
          </option>
        ))}
      </select>

    </div>
  );
};

export default RaceDropdown;