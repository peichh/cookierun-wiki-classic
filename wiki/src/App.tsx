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
  skill_description: string;
  description_th?: string;
  levels: CookieLevel[];
}

interface PetLevel {
  level: string;
  cooldown: string | null;
}

interface Pet {
  id: string;
  name: string;
  skill_description: string;
  description_th?: string;
  levels: PetLevel[];
}

const cookiesData = (cookiesDataRaw as Cookie[]).filter(c => c.name !== 'GingerBrave' || c.id === '100100');
const petsData = petsDataRaw as Pet[];

const CATEGORIES: Record<string, string[]> = {
  'ทำลายสิ่งกีดขวาง': ['GingerBrave', 'Muscle Cookie', 'Ninja Cookie', 'Knight Cookie', 'Pirate Cookie', 'Werewolf', 'Tiger Lily', 'Fire Spirit'],
  'เก็บเหรียญ': ['Buttercream Choco', 'Banana Cookie', 'Cheesecake Cookie', 'Mint Choco Cookie', 'Alchemist Cookie'],
  'ทำคะแนน': ['Strawberry Cookie', 'Skating Queen Cookie', 'Moonlight Cookie', 'Sea Fairy Cookie', 'Wind Archer Cookie'],
};

function formatCooldown(raw: string | null): string {
  if (!raw) return 'N/A';
  const val = parseFloat(raw);
  return (val / 100).toFixed(1) + 's';
}

function interpolateSkill(template: string, v1: string, v2: string): string {
  return template
    .replace('{V1}', v1 || '0')
    .replace('{V2}', v2 || '0')
    .replace('{0}', v1 || '0')
    .replace('{1}', v2 || '0');
}

export default function App() {
  const [search, setSearch] = useState('');
  const [tab, setTab] = useState<'cookies' | 'pets' | 'icetower'>('cookies');
  const [playstyle, setPlaystyle] = useState<string | null>(null);

  const filteredCookies = useMemo(() => {
    return cookiesData.filter(c => {
      const matchesSearch = c.name.toLowerCase().includes(search.toLowerCase()) || 
                           c.id.includes(search) || 
                           (c.description_th && c.description_th.includes(search));
      const matchesPlaystyle = !playstyle || CATEGORIES[playstyle]?.some(name => c.name.includes(name));
      return matchesSearch && matchesPlaystyle;
    });
  }, [search, playstyle]);

  const filteredPets = useMemo(() => {
    return petsData.filter(p => 
      p.name.toLowerCase().includes(search.toLowerCase()) || 
      p.id.includes(search) ||
      (p.description_th && p.description_th.includes(search))
    );
  }, [search]);

  if (tab === 'icetower') {
    return (
      <div className="min-h-screen bg-slate-950 font-serif">
        <nav className="bg-slate-900 border-b border-slate-800 p-4 sticky top-0 z-50">
          <div className="max-w-6xl mx-auto flex gap-4">
            <button onClick={() => setTab('cookies')} className="text-slate-400 hover:text-white text-sm font-bold transition-colors flex items-center gap-2">
              <span>←</span> กลับหน้าหลัก
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
          <p className="text-slate-400 font-bold tracking-widest text-xs uppercase">Technical Database &bull; ข้อมูลเชิงเทคนิค</p>
        </div>
        <button 
          onClick={() => setTab('icetower')}
          className="group relative px-8 py-3 bg-blue-700 hover:bg-blue-600 text-white rounded-none border-b-4 border-blue-900 text-sm font-black transition-all active:translate-y-1 active:border-b-0"
        >
          <span className="flex items-center gap-2">
            ❄️ ข้อมูลหอคอย (ICE TOWER)
          </span>
        </button>
      </header>

      <main className="max-w-6xl mx-auto space-y-12">
        {/* Search & Tabs */}
        <section className="space-y-6 bg-slate-900/30 p-6 border-2 border-slate-900">
          <div className="flex flex-col md:flex-row gap-4 items-center">
            <div className="relative flex-1 w-full">
              <input 
                type="text" 
                placeholder="ค้นหาชื่อ, ID หรือความสามารถ..."
                className="w-full bg-slate-950 border-2 border-slate-800 px-6 py-4 focus:outline-none focus:border-rose-500 transition-all font-bold"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <div className="flex bg-slate-950 border-2 border-slate-800 p-1">
              <button 
                onClick={() => setTab('cookies')}
                className={`px-8 py-2 font-black transition-all ${tab === 'cookies' ? 'bg-rose-600 text-white' : 'text-slate-500 hover:text-slate-300'}`}
              >คุกกี้</button>
              <button 
                onClick={() => setTab('pets')}
                className={`px-8 py-2 font-black transition-all ${tab === 'pets' ? 'bg-blue-600 text-white' : 'text-slate-500 hover:text-slate-300'}`}
              >สัตว์เลี้ยง</button>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            <button 
              onClick={() => setPlaystyle(null)}
              className={`px-4 py-1 text-[10px] font-black border-2 transition-all ${!playstyle ? 'bg-slate-100 border-slate-100 text-slate-950' : 'border-slate-800 text-slate-500 hover:border-slate-600'}`}
            >ทั้งหมด</button>
            {Object.keys(CATEGORIES).map(cat => (
              <button 
                key={cat}
                onClick={() => setPlaystyle(cat)}
                className={`px-4 py-1 text-[10px] font-black border-2 transition-all ${playstyle === cat ? 'bg-slate-100 border-slate-100 text-slate-950' : 'border-slate-800 text-slate-500 hover:border-slate-600'}`}
              >{cat.toUpperCase()}</button>
            ))}
          </div>
        </section>

        {/* Data Grid */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {tab === 'cookies' ? filteredCookies.map(cookie => {
            const maxLevel = cookie.levels[cookie.levels.length - 1];
            return (
              <div key={cookie.id} className="bg-slate-900/20 border-2 border-slate-900 p-6 hover:bg-slate-900/40 transition-all group flex flex-col h-full">
                <div className="flex justify-between items-start mb-6">
                  <div className="flex-1">
                    <span className="text-[10px] font-black text-rose-500 bg-rose-500/10 px-2 py-0.5 border border-rose-500/20">ID {cookie.id}</span>
                    <h3 className="text-2xl font-black mt-2 text-slate-100 tracking-tighter uppercase italic">{cookie.name}</h3>
                    {cookie.description_th && (
                      <p className="text-xs text-amber-400 font-bold mt-1 bg-amber-400/5 py-1 px-2 border-l-2 border-amber-400/50">
                        {cookie.description_th}
                      </p>
                    )}
                  </div>
                  <div className="bg-slate-950 border-2 border-slate-800 px-3 py-1 font-black text-emerald-400 text-sm">
                    {maxLevel.hp} HP
                  </div>
                </div>
                
                <div className="flex-1 space-y-4">
                  <div className="p-4 bg-slate-950 border-2 border-slate-900">
                    <span className="text-[10px] font-black text-slate-500 block mb-2 uppercase tracking-widest border-b border-slate-900 pb-1">ความสามารถ (เลเวลสูงสุด)</span>
                    <p className="text-sm text-slate-300 font-bold leading-relaxed">
                      {interpolateSkill(cookie.skill_description, maxLevel.skill_value_1, maxLevel.skill_value_2)}
                    </p>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t-2 border-slate-900 flex gap-4">
                  <div className="flex-1">
                    <span className="text-[9px] font-black text-slate-600 uppercase">ค่าตัวแปร 1</span>
                    <div className="text-lg font-black text-rose-500 italic">{maxLevel.skill_value_1 || '—'}</div>
                  </div>
                  <div className="flex-1">
                    <span className="text-[9px] font-black text-slate-600 uppercase">ค่าตัวแปร 2</span>
                    <div className="text-lg font-black text-orange-500 italic">{maxLevel.skill_value_2 || '—'}</div>
                  </div>
                </div>
              </div>
            )
          }) : filteredPets.map(pet => {
            const maxLevel = pet.levels[pet.levels.length - 1];
            return (
              <div key={pet.id} className="bg-slate-900/20 border-2 border-slate-900 p-6 hover:bg-slate-900/40 transition-all group flex flex-col h-full">
                <div className="flex justify-between items-start mb-6">
                  <div className="flex-1">
                    <span className="text-[10px] font-black text-blue-500 bg-blue-500/10 px-2 py-0.5 border border-blue-500/20">ID {pet.id}</span>
                    <h3 className="text-2xl font-black mt-2 text-slate-100 tracking-tighter uppercase italic">{pet.name}</h3>
                    {pet.description_th && (
                      <p className="text-xs text-blue-400 font-bold mt-1 bg-blue-400/5 py-1 px-2 border-l-2 border-blue-400/50">
                        {pet.description_th}
                      </p>
                    )}
                  </div>
                  <div className="bg-slate-950 border-2 border-slate-800 px-3 py-1 font-black text-sky-400 text-sm">
                    {formatCooldown(maxLevel.cooldown)} CD
                  </div>
                </div>
                <div className="flex-1 space-y-4">
                  <div className="p-4 bg-slate-950 border-2 border-slate-900 h-full">
                    <span className="text-[10px] font-black text-slate-500 block mb-2 uppercase tracking-widest border-b border-slate-900 pb-1">ความสามารถสัตว์เลี้ยง</span>
                    <p className="text-sm text-slate-300 font-bold leading-relaxed">
                      {pet.skill_description}
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
        </section>
      </main>

      <footer className="max-w-6xl mx-auto mt-20 pt-8 border-t-4 border-slate-900 text-center text-slate-600 text-[10px] font-black uppercase tracking-widest">
        &copy; 2026 COOKIERUN TECHNICAL WIKI &bull; POWERED BY POKE &bull; DESIGNED FOR COLLECTORS
      </footer>
    </div>
  );
}
