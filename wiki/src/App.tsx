import { useState, useMemo } from 'react';
import cookiesDataRaw from './data/cookies_rich.json';
import petsDataRaw from './data/pets_rich.json';
import IceTowerPage from './IceTowerPage';

interface CookieLevel {
  level: string;
  hp: string | null;
  skill_value_1: string;
  skill_value_2: string;
}

interface Cookie {
  id: string;
  name: string;
  skill_description_en: string;
  skill_description_th: string;
  levels: CookieLevel[];
}

interface PetLevel {
  level: string;
  cooldown: string | null;
}

interface Pet {
  id: string;
  name: string;
  skill_description_en: string;
  skill_description_th: string;
  levels: PetLevel[];
}

const cookiesData = (cookiesDataRaw as Cookie[]).filter(c => c.name !== 'GingerBrave' || c.id === '100100');
const petsData = petsDataRaw as Pet[];

const CATEGORIES: Record<string, string[]> = {
  'ทำลายสิ่งกีดขวาง': ['GingerBrave', 'Muscle Cookie', 'Ninja Cookie', 'Knight Cookie', 'Pirate Cookie', 'Werewolf', 'Tiger Lily', 'Fire Spirit'],
  'เก็บเหรียญ': ['Buttercream Choco', 'Banana Cookie', 'Cheesecake Cookie', 'Mint Choco Cookie', 'Alchemist Cookie', 'Potato Salad'],
  'ทำคะแนน': ['Strawberry Cookie', 'Skating Queen Cookie', 'Moonlight Cookie', 'Sea Fairy Cookie', 'Wind Archer Cookie'],
};

function formatCooldown(raw: string | null): string {
  if (!raw) return 'N/A';
  const val = parseFloat(raw);
  return (val / 100).toFixed(1) + 's';
}

function interpolateSkill(template: string, v1: string, v2: string): string {
  return template
    .replace(/{V1}/g, v1 || '0')
    .replace(/{V2}/g, v2 || '0')
    .replace(/\{0\}/g, v1 || '0')
    .replace(/\{1\}/g, v2 || '0');
}

export default function App() {
  const [search, setSearch] = useState('');
  const [tab, setTab] = useState<'cookies' | 'pets' | 'icetower'>('cookies');
  const [playstyle, setPlaystyle] = useState<string | null>(null);

  const filteredCookies = useMemo(() => {
    return cookiesData.filter(c => {
      const matchesSearch = c.name.toLowerCase().includes(search.toLowerCase()) || 
                           (c.skill_description_th && c.skill_description_th.includes(search));
      const matchesPlaystyle = !playstyle || CATEGORIES[playstyle]?.some(name => c.name.includes(name));
      return matchesSearch && matchesPlaystyle;
    });
  }, [search, playstyle]);

  const filteredPets = useMemo(() => {
    return petsData.filter(p => 
      p.name.toLowerCase().includes(search.toLowerCase()) || 
      (p.skill_description_th && p.skill_description_th.includes(search))
    );
  }, [search]);

  if (tab === 'icetower') {
    return (
      <div className="min-h-screen bg-slate-950 font-serif">
        <nav className="bg-slate-900 border-b border-slate-800 p-4 sticky top-0 z-50">
          <div className="max-w-6xl mx-auto flex gap-4">
            <button onClick={() => setTab('cookies')} className="text-slate-400 hover:text-white text-sm font-bold transition-colors flex items-center gap-2">
              <span>←</span> กลับหน้าหลัก (Back to Wiki)
            </button>
          </div>
        </nav>
        <IceTowerPage />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8 font-serif selection:bg-rose-500/30">
      <header className="max-w-6xl mx-auto mb-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 border-b-4 border-slate-900 pb-8">
        <div>
          <h1 className="text-5xl font-black bg-gradient-to-r from-orange-400 via-rose-500 to-fuchsia-600 bg-clip-text text-transparent mb-3 tracking-tighter uppercase italic">
            CookieRun Wiki
          </h1>
          <p className="text-slate-400 font-bold tracking-widest text-xs uppercase">ข้อมูลกลไกการเล่นแบบละเอียด &bull; Detailed Technical Specs</p>
        </div>
        <button 
          onClick={() => setTab('icetower')}
          className="group relative px-8 py-3 bg-blue-700 hover:bg-blue-600 text-white rounded-none border-b-4 border-blue-900 text-sm font-black transition-all active:translate-y-1 active:border-b-0"
        >
          <span className="flex items-center gap-2">
            ❄️ หอคอยร้อยชั้น (ICE TOWER)
          </span>
        </button>
      </header>

      <main className="max-w-7xl mx-auto space-y-12">
        {/* Filter Section */}
        <section className="bg-slate-900/30 p-8 border-2 border-slate-900 space-y-6">
          <div className="flex flex-col md:flex-row gap-6 items-center">
            <div className="relative flex-1 w-full">
              <input 
                type="text" 
                placeholder="ค้นหาชื่อคุกกี้ หรือความสามารถ (เช่น 'ขี่มอเตอร์ไซค์', 'คืนชีพ')..."
                className="w-full bg-slate-950 border-2 border-slate-800 px-6 py-4 focus:outline-none focus:border-rose-500 transition-all font-bold text-lg"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <div className="flex bg-slate-950 border-2 border-slate-800 p-1">
              <button 
                onClick={() => setTab('cookies')}
                className={`px-10 py-3 font-black transition-all ${tab === 'cookies' ? 'bg-rose-600 text-white' : 'text-slate-500 hover:text-slate-300'}`}
              >คุกกี้</button>
              <button 
                onClick={() => setTab('pets')}
                className={`px-10 py-3 font-black transition-all ${tab === 'pets' ? 'bg-blue-600 text-white' : 'text-slate-500 hover:text-slate-300'}`}
              >สัตว์เลี้ยง</button>
            </div>
          </div>
          <div className="flex flex-wrap gap-3">
            <button 
              onClick={() => setPlaystyle(null)}
              className={`px-6 py-2 text-xs font-black border-2 transition-all ${!playstyle ? 'bg-slate-100 border-slate-100 text-slate-950' : 'border-slate-800 text-slate-500 hover:border-slate-600'}`}
            >แสดงทั้งหมด</button>
            {Object.keys(CATEGORIES).map(cat => (
              <button 
                key={cat}
                onClick={() => setPlaystyle(cat)}
                className={`px-6 py-2 text-xs font-black border-2 transition-all ${playstyle === cat ? 'bg-slate-100 border-slate-100 text-slate-950' : 'border-slate-800 text-slate-500 hover:border-slate-600'}`}
              >{cat.toUpperCase()}</button>
            ))}
          </div>
        </section>

        {/* Technical Data Grid */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {tab === 'cookies' ? filteredCookies.map(cookie => {
            const maxLevel = cookie.levels[cookie.levels.length - 1];
            return (
              <div key={cookie.id} className="bg-slate-950 border-2 border-slate-900 hover:border-rose-500/50 transition-all flex flex-col overflow-hidden group shadow-xl">
                <div className="p-6 bg-slate-900/40 border-b-2 border-slate-900 flex justify-between items-center">
                  <h3 className="text-3xl font-black italic tracking-tighter text-slate-100 uppercase group-hover:text-rose-500 transition-colors">
                    {cookie.name}
                  </h3>
                  <div className="bg-slate-950 border-2 border-slate-800 px-4 py-2 font-black text-emerald-400">
                    {maxLevel.hp} HP
                  </div>
                </div>
                
                <div className="p-8 flex-1 space-y-8">
                  <div>
                    <span className="text-[10px] font-black text-rose-500 uppercase tracking-[0.2em] mb-4 block border-b-2 border-rose-500/20 pb-2">คำอธิบายกลไกการเล่น (Technical Mechanics)</span>
                    <p className="text-lg text-slate-200 font-bold leading-relaxed indent-8">
                      {interpolateSkill(cookie.skill_description_th, maxLevel.skill_value_1, maxLevel.skill_value_2)}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-6 bg-slate-900/20 p-6 border-2 border-slate-900">
                    <div>
                      <span className="text-[9px] font-black text-slate-600 uppercase tracking-widest block mb-2">ตัวแปรความสามารถ 1</span>
                      <div className="text-2xl font-black text-rose-500 italic">{maxLevel.skill_value_1 || '—'}</div>
                    </div>
                    <div>
                      <span className="text-[9px] font-black text-slate-600 uppercase tracking-widest block mb-2">ตัวแปรความสามารถ 2</span>
                      <div className="text-2xl font-black text-orange-500 italic">{maxLevel.skill_value_2 || '—'}</div>
                    </div>
                  </div>
                </div>

                <div className="px-8 py-4 bg-slate-900/10 text-[10px] text-slate-700 font-black flex justify-between italic uppercase">
                  <span>CookieRun Technical Manual</span>
                  <span>Section: {cookie.name.replace(' ', '_')}</span>
                </div>
              </div>
            )
          }) : filteredPets.map(pet => {
            const maxLevel = pet.levels[pet.levels.length - 1];
            return (
              <div key={pet.id} className="bg-slate-950 border-2 border-slate-900 hover:border-blue-500/50 transition-all flex flex-col overflow-hidden group shadow-xl">
                <div className="p-6 bg-slate-900/40 border-b-2 border-slate-900 flex justify-between items-center">
                  <h3 className="text-3xl font-black italic tracking-tighter text-slate-100 uppercase group-hover:text-blue-500 transition-colors">
                    {pet.name}
                  </h3>
                  <div className="bg-slate-950 border-2 border-slate-800 px-4 py-2 font-black text-sky-400">
                    {formatCooldown(maxLevel.cooldown)} CD
                  </div>
                </div>
                
                <div className="p-8 flex-1">
                  <span className="text-[10px] font-black text-blue-500 uppercase tracking-[0.2em] mb-4 block border-b-2 border-blue-500/20 pb-2">ความสามารถสัตว์เลี้ยง (Pet Skill)</span>
                  <p className="text-lg text-slate-200 font-bold leading-relaxed indent-8">
                    {pet.skill_description_th}
                  </p>
                </div>

                <div className="px-8 py-4 bg-slate-900/10 text-[10px] text-slate-700 font-black flex justify-between italic uppercase">
                  <span>Pet System Manual</span>
                  <span>Module: {pet.name.replace(' ', '_')}</span>
                </div>
              </div>
            )
          })}
        </section>
      </main>

      <footer className="max-w-6xl mx-auto mt-20 pt-10 border-t-4 border-slate-900 text-center space-y-4 pb-12">
        <div className="text-slate-600 text-[10px] font-black uppercase tracking-[0.5em]">
          &copy; 2026 COOKIERUN TECHNICAL WIKI &bull; POWERED BY POKE
        </div>
        <div className="text-slate-800 text-[8px] font-black uppercase">
          Authorized for collector use only &bull; data source: derived_json_v3
        </div>
      </footer>
    </div>
  );
}
