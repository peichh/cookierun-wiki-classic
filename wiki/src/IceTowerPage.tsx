import React from 'react';

interface Mission {
  id: number;
  type: string;
  condition: string;
  reward: string;
}

const missions: Mission[] = [
  { id: 1, type: 'Score', condition: 'Reach 1,000,000 points', reward: '10 Crystals' },
  { id: 2, type: 'Coins', condition: 'Collect 5,000 coins', reward: '2,000 Coins' },
  { id: 3, type: 'Jellies', condition: 'Collect 500 Yellow Jellies', reward: '1 Gift Point' },
  // Add more missions as needed
];

export default function IceTowerPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8 font-sans">
      <header className="max-w-6xl mx-auto mb-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-500 bg-clip-text text-transparent mb-2">
          Tower of Frozen Waves
        </h1>
        <p className="text-slate-400">Mission and Reward Data for the Ice Tower</p>
      </header>

      <main className="max-w-6xl mx-auto">
        <section className="bg-slate-900/50 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur-sm">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-800/50 text-slate-400 text-xs uppercase tracking-wider">
                <th className="px-6 py-4 font-semibold">Floor</th>
                <th className="px-6 py-4 font-semibold">Mission Type</th>
                <th className="px-6 py-4 font-semibold">Requirement</th>
                <th className="px-6 py-4 font-semibold">Reward</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {missions.map((m) => (
                <tr key={m.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-6 py-4 font-mono text-sm">{m.id}F</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 rounded bg-blue-500/10 text-blue-400 text-xs font-medium border border-blue-500/20">
                      {m.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-300">{m.condition}</td>
                  <td className="px-6 py-4 text-sm font-bold text-emerald-400">{m.reward}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}
