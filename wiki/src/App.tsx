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
  description_th: string;
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
  description_th: string;
  levels: PetLevel[];
}

const cookiesData = cookiesDataRaw as Cookie[];
const petsData = petsDataRaw as Pet[];

const CATEGORIES: Record<string, string[]> = {
  'Obstacle Destruction': ['GingerBrave', 'Muscle Cookie', 'Ninja Cookie', 'Knight Cookie', 'Pirate Cookie', 'Werewolf', 'Tiger Lily', 'Fire Spirit'],
  'Coin Farming': ['Buttercream Choco', 'Banana Cookie', 'Cheesecake Cookie', 'Mint Choco Cookie', 'Alchemist Cookie'],
  'High Score': ['Strawberry Cookie', 'Skating Queen Cookie', 'Moonlight Cookie', 'Sea Fairy Cookie', 'Wind Archer Cookie'],
};

function formatCooldown(raw: string | null): string {
  if (!raw) return 'N/A';
  const val = parseFloat(raw);
  // Rule: Cooldown 1000 -> 10.0s (deciseconds/100 or frames/60, based on Choco Drop 1000)
  // Standardizing on /100 for now which matches most common data dumps
  return (val / 100).toFixed(1) + 's';
}

export default function App() {
  const [search, setSearch] = useState('');
  const [tab, setTab] = useState<'cookies' | 'pets' | 'icetower'>('cookies');
  const [playstyle, setPlaystyle] = useState<string | null>(null);

  const filteredCookies = useMemo(() => {
    return cookiesData.filter(c => {
      const matchesSearch = c.name.toLowerCase().includes(search.toLowerCase()) || c.id.includes(search);
      const matchesPlaystyle = !playstyle || CATEGORIES[playstyle]?.some(name => c.name.includes(name));
      return matchesSearch && matchesPlaystyle;
    });
  }, [search, playstyle]);

  const filteredPets = useMemo(() => {
    return petsData.filter(p => p.name.toLowerCase().includes(search.toLowerCase()) || p.id.includes(search));
  }, [search]);

  if (tab === 'icetower') {
    return (
      <>
        <nav className="bg-slate-900 border-b border-slate-800 p-4 sticky top-0 z-50">
          <div className="max-w-6xl mx-auto flex gap-4">
            <button onClick={() => setTab('cookies')} className="text-slate-400 hover:text-white text-sm font-medium transition-colors flex items-center gap-2">
              <span>←</span> Back to Wiki
            </button>
          </div>
        </nav>
        <IceTowerPage />
      </>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8 font-sans selection:bg-rose-500/30">
      <header className="max-w-6xl mx-auto mb-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h1 className="text-5xl font-black bg-gradient-to-r from-orange-400 via-rose-500 to-fuchsia-600 bg-clip-text text-transparent mb-3 tracking-tight">
            CookieRun Wiki
          </h1>
          <p className="text-slate-400 font-medium">Professional grade technical database</p>
        </div>
        <button 
          onClick={() => setTab('icetower')}
          className="group relative px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-2xl text-sm font-bold shadow-xl shadow-blue-900/40 transition-all hover:-translate-y-0.5 active:translate-y-0"
        >
          <span className="flex items-center gap-2">
            <span className="text-lg">❄️</span> Ice Tower Data
          </span>
        </button>
      </header>

      <main className="max-w-6xl mx-auto space-y-12">
        {/* Search & Tabs */}
        <section className="space-y-6">
          <div className="flex flex-col md:flex-row gap-4 items-center">
            <div className="relative flex-1 w-full">
              <input 
                type="text" 
                placeholder="Search by name or ID..."
                className="w-full bg-slate-900/80 border border-slate-700/50 rounded-2xl px-6 py-4 focus:outline-none focus:ring-2 focus:ring-rose-500/50 transition-all backdrop-blur-xl"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <div className="flex bg-slate-900/80 rounded-2xl p-1.5 border border-slate-800 shadow-inner">
              <button 
                onClick={() => setTab('cookies')}
                className={`px-8 py-2.5 rounded-xl font-bold transition-all ${tab === 'cookies' ? 'bg-slate-800 text-white shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
              >Cookies</button>
              <button 
                onClick={() => setTab('pets')}
                className={`px-8 py-2.5 rounded-xl font-bold transition-all ${tab === 'pets' ? 'bg-slate-800 text-white shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
              >Pets</button>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            <button 
              onClick={() => setPlaystyle(null)}
              className={`px-5 py-2 rounded-xl text-xs font-bold border transition-all ${!playstyle ? 'bg-rose-500 border-rose-500 text-white' : 'border-slate-800 text-slate-400 hover:border-slate-600'}`}
            >All</button>
            {Object.keys(CATEGORIES).map(cat => (
              <button 
                key={cat}
                onClick={() => setPlaystyle(cat)}
                className={`px-5 py-2 rounded-xl text-xs font-bold border transition-all ${playstyle === cat ? 'bg-orange-500 border-orange-500 text-white' : 'border-slate-800 text-slate-400 hover:border-slate-600'}`}
              >{cat}</button>
            ))}
          </div>
        </section>

        {/* Data Grid */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tab === 'cookies' ? filteredCookies.map(cookie => {
            const maxLevel = cookie.levels[cookie.levels.length - 1];
            return (
              <div key={cookie.id} className="bg-slate-900/40 border border-slate-800/80 rounded-3xl p-6 hover:border-rose-500/30 transition-all group relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                  <span className="text-4xl font-black">🍪</span>
                </div>
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest bg-slate-800/50 px-2 py-0.5 rounded-md">ID {cookie.id}</span>
                    <h3 className="text-xl font-black mt-2 group-hover:text-rose-400 transition-colors tracking-tight">{cookie.name}</h3>
                    <p className="text-xs text-slate-400 mt-1 line-clamp-1">{cookie.description_th}</p>
                  </div>
                  <div className="bg-slate-800/80 border border-slate-700/50 px-3 py-1 rounded-xl text-xs font-black text-emerald-400">
                    {maxLevel.hp} HP
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="p-4 bg-slate-950/80 rounded-2xl border border-slate-800/50">
                    <span className="text-[10px] font-bold text-slate-500 block mb-2 uppercase tracking-wider">Passive Skill (Max Level)</span>
                    <p className="text-sm text-slate-200 font-medium leading-relaxed">
                      {cookie.skill_description.replace('{V1}', maxLevel.skill_value_1 || '0').replace('{V2}', maxLevel.skill_value_2 || '0')}
                    </p>
                  </div>
                  <div className="flex gap-4 px-2">
                    <div className="flex-1">
                      <span className="text-[9px] font-bold text-slate-600 uppercase">Var 1</span>
                      <div className="text-sm font-mono font-bold text-rose-400">{maxLevel.skill_value_1 || '—'}</div>
                    </div>
                    <div className="flex-1">
                      <span className="text-[9px] font-bold text-slate-600 uppercase">Var 2</span>
                      <div className="text-sm font-mono font-bold text-orange-400">{maxLevel.skill_value_2 || '—'}</div>
                    </div>
                  </div>
                </div>
              </div>
            )
          }) : filteredPets.map(pet => {
            const maxLevel = pet.levels[pet.levels.length - 1];
            return (
              <div key={pet.id} className="bg-slate-900/40 border border-slate-800/80 rounded-3xl p-6 hover:border-sky-500/30 transition-all group relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                  <span className="text-4xl font-black">🐾</span>
                </div>
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest bg-slate-800/50 px-2 py-0.5 rounded-md">ID {pet.id}</span>
                    <h3 className="text-xl font-black mt-2 group-hover:text-sky-400 transition-colors tracking-tight">{pet.name}</h3>
                    <p className="text-xs text-slate-400 mt-1 line-clamp-1">{pet.description_th}</p>
                  </div>
                  <div className="bg-slate-800/80 border border-slate-700/50 px-3 py-1 rounded-xl text-xs font-black text-sky-400">
                    {formatCooldown(maxLevel.cooldown)} CD
                  </div>
                </div>
                <div className="p-4 bg-slate-950/80 rounded-2xl border border-slate-800/50">
                  <span className="text-[10px] font-bold text-slate-500 block mb-2 uppercase tracking-wider">Active Ability</span>
                  <p className="text-sm text-slate-200 font-medium leading-relaxed">
                    {pet.skill_description}
                  </p>
                </div>
              </div>
            )
          })}
        </section>
      </main>

      <footer className="max-w-6xl mx-auto mt-20 pt-8 border-t border-slate-900 text-center text-slate-600 text-xs font-medium">
        &copy; 2026 CookieRun Technical Wiki &bull; Processed by Poke
      </footer>
    </div>
  );
}
