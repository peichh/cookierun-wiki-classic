import { useState, useMemo } from 'react';
import cookiesDataRaw from './data/cookies_rich.json';
import petsDataRaw from './data/pets_rich.json';

// Simple types for Classic CookieRun
interface Cookie {
  id: string;
  name: string;
  levels: { hp: string | null; skill_value_1: string; skill_value_2: string }[];
}

interface Pet {
  id: string;
  name: string;
  levels: { cooldown: string | null }[];
}

const cookiesData = cookiesDataRaw as Cookie[];
const petsData = petsDataRaw as Pet[];

// Utility mapping based on known archetypes for filtering
const CATEGORIES: Record<string, string[]> = {
  'Obstacle Destruction': ['GingerBrave', 'Muscle Cookie', 'Ninja Cookie', 'Knight Cookie', 'Pirate Cookie', 'Muscle', 'Ninja', 'Knight', 'Pirate', 'Werewolf', 'Tiger Lily', 'Fire Spirit'],
  'Coin Farming': ['Buttercream Choco', 'Banana Cookie', 'Cheesecake Cookie', 'Mint Choco Cookie', 'Alchemist Cookie', 'Buttercream', 'Banana', 'Cheesecake', 'Mint Choco', 'Alchemist'],
  'High Score': ['Strawberry Cookie', 'Skating Queen Cookie', 'Moonlight Cookie', 'Sea Fairy Cookie', 'Wind Archer Cookie', 'Skating Queen', 'Moonlight', 'Sea Fairy', 'Wind Archer'],
};

export default function App() {
  const [search, setSearch] = useState('');
  const [tab, setTab] = useState<'cookies' | 'pets'>('cookies');
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

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8 font-sans">
      <header className="max-w-6xl mx-auto mb-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-orange-400 to-rose-500 bg-clip-text text-transparent mb-2">
          CookieRun Technical Wiki
        </h1>
        <p className="text-slate-400">Authentic technical data for CookieRun Classic</p>
      </header>

      <main className="max-w-6xl mx-auto space-y-8">
        {/* Core Physics Card */}
        <section className="bg-slate-900/50 border border-slate-800 rounded-2xl p-6 backdrop-blur-sm">
          <h2 className="text-xl font-semibold mb-4 text-orange-400 flex items-center gap-2">
            ⚙️ Core Physics Reference
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-sm">
            <div className="space-y-1">
              <span className="text-slate-500 block uppercase tracking-wider text-xs">Gravity</span>
              <span className="text-xl font-mono">0.8</span>
            </div>
            <div className="space-y-1">
              <span className="text-slate-500 block uppercase tracking-wider text-xs">Jump Velocity</span>
              <span className="text-xl font-mono">14.5</span>
            </div>
            <div className="space-y-1">
              <span className="text-slate-500 block uppercase tracking-wider text-xs">Double Jump</span>
              <span className="text-xl font-mono">12.0</span>
            </div>
            <div className="space-y-1">
              <span className="text-slate-500 block uppercase tracking-wider text-xs">Health Drain</span>
              <span className="text-xl font-mono">1 HP/s</span>
            </div>
          </div>
        </section>

        {/* Search & Filters */}
        <section className="space-y-4">
          <div className="flex flex-col md:flex-row gap-4">
            <input 
              type="text" 
              placeholder="Search by name or ID..."
              className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-rose-500/50 transition-all"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            <div className="flex bg-slate-900 rounded-xl p-1 border border-slate-800">
              <button 
                onClick={() => setTab('cookies')}
                className={`px-6 py-2 rounded-lg transition-all ${tab === 'cookies' ? 'bg-slate-800 text-white shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
              >Cookies</button>
              <button 
                onClick={() => setTab('pets')}
                className={`px-6 py-2 rounded-lg transition-all ${tab === 'pets' ? 'bg-slate-800 text-white shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
              >Pets</button>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            <button 
              onClick={() => setPlaystyle(null)}
              className={`px-4 py-1.5 rounded-full text-xs font-medium border transition-all ${!playstyle ? 'bg-rose-500 border-rose-500 text-white' : 'border-slate-800 text-slate-400 hover:border-slate-600'}`}
            >All</button>
            {Object.keys(CATEGORIES).map(cat => (
              <button 
                key={cat}
                onClick={() => setPlaystyle(cat)}
                className={`px-4 py-1.5 rounded-full text-xs font-medium border transition-all ${playstyle === cat ? 'bg-orange-500 border-orange-500 text-white' : 'border-slate-800 text-slate-400 hover:border-slate-600'}`}
              >{cat}</button>
            ))}
          </div>
        </section>

        {/* Data List */}
        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tab === 'cookies' ? filteredCookies.map(cookie => {
            const maxLevel = cookie.levels[cookie.levels.length - 1];
            return (
              <div key={cookie.id} className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all group">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">#{cookie.id}</span>
                    <h3 className="text-lg font-bold group-hover:text-rose-400 transition-colors">{cookie.name}</h3>
                  </div>
                  <div className="bg-slate-800 px-3 py-1 rounded-lg text-xs font-bold text-emerald-400">
                    {maxLevel.hp} HP
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/50 text-sm text-slate-300">
                    <span className="text-[10px] text-slate-500 block mb-1 uppercase">Max Skill Values</span>
                    <div className="flex gap-4 font-mono text-xs">
                      <span>V1: {maxLevel.skill_value_1 || '0'}</span>
                      <span>V2: {maxLevel.skill_value_2 || '0'}</span>
                    </div>
                  </div>
                </div>
              </div>
            )
          }) : filteredPets.map(pet => {
            const maxLevel = pet.levels[pet.levels.length - 1];
            return (
              <div key={pet.id} className="bg-slate-900/40 border border-slate-800 rounded-2xl p-5 hover:border-slate-700 transition-all group">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">#{pet.id}</span>
                    <h3 className="text-lg font-bold group-hover:text-orange-400 transition-colors">{pet.name}</h3>
                  </div>
                  <div className="bg-slate-800 px-3 py-1 rounded-lg text-xs font-bold text-sky-400">
                    {maxLevel.cooldown} CD
                  </div>
                </div>
              </div>
            )
          })}
        </section>
      </main>
    </div>
  );
}
