import React from "react";

function App() {
  return (
    <div className="min-h-screen bg-f1bg text-white font-f1">
      {/* NAVBAR */}
      <nav className="bg-black px-6 py-4 flex justify-between items-center shadow-md border-b border-gray-800">
        <h1 className="text-f1red text-3xl font-bold tracking-widest">
          PITFORSTATS
        </h1>
        <ul className="flex space-x-6 text-gray-300 text-sm">
          <li className="hover:text-white cursor-pointer">Overview</li>
          <li className="hover:text-white cursor-pointer">Races</li>
          <li className="hover:text-white cursor-pointer">Drivers</li>
          <li className="hover:text-white cursor-pointer">Insights</li>
        </ul>
      </nav>

      {/* DASHBOARD GRID */}
      <main className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* CARD 1 */}
        <div className="bg-[#1a1a1a] p-5 rounded-2xl shadow-inner border border-gray-700">
          <h2 className="text-lg font-semibold text-f1red mb-2">Fastest Lap</h2>
          <p className="text-2xl font-bold">1:31.620</p>
          <p className="text-sm text-gray-400">By Max Verstappen | Bahrain GP</p>
        </div>

        {/* CARD 2 */}
        <div className="bg-[#1a1a1a] p-5 rounded-2xl shadow-inner border border-gray-700">
          <h2 className="text-lg font-semibold text-f1red mb-2">Avg Pit Stop</h2>
          <p className="text-2xl font-bold">2.31 sec</p>
          <p className="text-sm text-gray-400">Red Bull Racing</p>
        </div>

        {/* CARD 3 */}
        <div className="col-span-1 md:col-span-2 bg-[#1a1a1a] p-5 rounded-2xl border border-gray-700">
          <h2 className="text-lg font-semibold text-f1red mb-4">Lap Time Comparison</h2>
          <div className="h-64 flex items-center justify-center text-gray-500 italic">
            [Insert Lap Time Chart Here]
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
