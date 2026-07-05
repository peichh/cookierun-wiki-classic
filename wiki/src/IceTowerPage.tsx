import React from 'react';
import missionsRaw from './data/ice_tower_missions.json';

interface MissionDetail {
  desc_ko: string;
  desc_en: string;
  reward: string;
  target: string;
  key: string;
}

interface StageMission {
  stage: number;
  mission1: MissionDetail;
  mission2: MissionDetail;
  mission3: MissionDetail;
}

const missions = missionsRaw as StageMission[];

export default function IceTowerPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8 font-sans">
      <header className="max-w-6xl mx-auto mb-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-cyan-500 bg-clip-text text-transparent mb-2">
          Tower of Frozen Waves
        </h1>
        <p className="text-slate-400">Mission and Reward Data for all 100 Floors</p>
      </header>

      <main className="max-w-6xl mx-auto">
        <section className="bg-slate-900/50 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur-sm shadow-2xl">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-800/80 text-slate-400 text-xs uppercase tracking-wider">
                <th className="px-6 py-4 font-semibold border-b border-slate-700">Floor</th>
                <th className="px-6 py-4 font-semibold border-b border-slate-700">Mission 1 (Crystal/Key)</th>
                <th className="px-6 py-4 font-semibold border-b border-slate-700">Mission 2</th>
                <th className="px-6 py-4 font-semibold border-b border-slate-700">Mission 3</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {missions.map((m) => (
                <tr key={m.stage} className="hover:bg-slate-800/30 transition-colors group">
                  <td className="px-6 py-4 font-mono text-sm font-bold text-blue-400 bg-slate-800/20">{m.stage}F</td>
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-slate-200">{m.mission1.desc_en}</div>
                    <div className="text-xs text-emerald-400 mt-1 font-bold">🎁 {m.mission1.reward}</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-slate-300">{m.mission2.desc_en}</div>
                    <div className="text-xs text-slate-500 mt-1">{m.mission2.reward}</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-slate-300">{m.mission3.desc_en}</div>
                    <div className="text-xs text-slate-500 mt-1">{m.mission3.reward}</div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}
