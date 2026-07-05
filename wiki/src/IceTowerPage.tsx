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
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8 font-serif">
      <header className="max-w-6xl mx-auto mb-12 flex flex-col md:flex-row justify-between items-end border-b-4 border-slate-900 pb-8">
        <div>
          <h1 className="text-5xl font-black bg-gradient-to-r from-blue-400 to-cyan-500 bg-clip-text text-transparent mb-2 tracking-tighter uppercase italic">
            Tower of Frozen Waves
          </h1>
          <p className="text-slate-400 font-black uppercase text-xs tracking-widest">หอคอยคลื่นยักษ์ &bull; ข้อมูลภารกิจและของรางวัล</p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto">
        <section className="bg-slate-950 border-2 border-slate-900 overflow-hidden shadow-2xl">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-900/50 text-slate-500 text-[10px] font-black uppercase tracking-widest">
                <th className="px-6 py-4 border-b-2 border-slate-900">ชั้น (Floor)</th>
                <th className="px-6 py-4 border-b-2 border-slate-900">ภารกิจ 1 (คริสตัล/กุญแจ)</th>
                <th className="px-6 py-4 border-b-2 border-slate-900">ภารกิจ 2</th>
                <th className="px-6 py-4 border-b-2 border-slate-900">ภารกิจ 3</th>
              </tr>
            </thead>
            <tbody className="divide-y-2 divide-slate-900">
              {missions.map((m) => (
                <tr key={m.stage} className="hover:bg-slate-900/20 transition-colors group">
                  <td className="px-6 py-4 font-black text-lg italic text-blue-500 bg-slate-900/10 border-r-2 border-slate-900 w-24 text-center">
                    {m.stage}F
                  </td>
                  <td className="px-6 py-4 border-r-2 border-slate-900">
                    <div className="text-sm font-bold text-slate-200 leading-tight">{m.mission1.desc_en}</div>
                    <div className="text-[10px] text-emerald-400 mt-2 font-black uppercase bg-emerald-400/10 px-2 py-0.5 inline-block border border-emerald-400/20">
                       {m.mission1.reward}
                    </div>
                  </td>
                  <td className="px-6 py-4 border-r-2 border-slate-900">
                    <div className="text-sm font-bold text-slate-400 leading-tight">{m.mission2.desc_en}</div>
                    <div className="text-[10px] text-slate-600 mt-2 font-black uppercase">{m.mission2.reward}</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm font-bold text-slate-400 leading-tight">{m.mission3.desc_en}</div>
                    <div className="text-[10px] text-slate-600 mt-2 font-black uppercase">{m.mission3.reward}</div>
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
