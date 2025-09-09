import { BarChart3, LayoutDashboard } from "lucide-react";
import Sidebar, { SidebarItem } from "./components/Sidebar";

function App() {
  return (
    <main className="app-container flex">
      <Sidebar>
        <SidebarItem icon={<LayoutDashboard size={20} />} text="Dashboard" alert />
        <SidebarItem icon={<BarChart3 size={20} />} text="Previous Results" />
      </Sidebar>
    </main>
  );
}

export default App;
