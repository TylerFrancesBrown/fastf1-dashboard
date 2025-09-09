import React from "react";
import { ChevronFirst } from "lucide-react";
import F1Logo from "../assets/F1.svg";

export default function Sidebar({ children }) {
  return (
    <aside className="h-screen">
      <nav className="h-full flex flex-col bg-white border-r shadow-sm">
        <div className="p-4 pb-2 flex justify-between items-center">
          <img src={F1Logo} className="w-8 h-8" alt="logo" />
          <button className="p-1.5 rounded-lg bg-gray-50 hover:bg-gray-100">
            <ChevronFirst />
          </button>
        </div>

        <ul className="flex-1 px-3">{children}</ul>
      </nav>
    </aside>
  );
}

export function SidebarItem({ icon, text, active, alert }) {
  return (
    <li
      className={`
        relative flex items-center gap-2 py-2 px-3 my-1
        font-medium rounded-md cursor-pointer 
        transition-colors
        ${
          active
            ? "bg-gradient-to-tr from-indigo-200 to-indigo-100 text-indigo-800"
            : "hover:bg-indigo-50 text-gray-600"
        }
      `}
    >
      {icon}
      <span className="flex-1">{text}</span>

      {alert && (
        <span className="absolute right-2 w-2 h-2 rounded-full bg-red-500"></span>
      )}
    </li>
  );
}
