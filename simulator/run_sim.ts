import { CookieRunSimulator } from './simulator.ts';
import { SimConfig } from './types.ts';

const basePlayer = {
  heartLevel: 60,
  jellyLevel: 70,
  bonusTimeLevel: 70,
  userLevel: 100,
  hp: 0
};

const baseConfig: SimConfig = {
  player: basePlayer,
  boosters: ['Quick Start', 'Health Boost', 'Double XP'],
  randomBoost: '-15% HP drain',
  crashTimestamps: [],
  episodeMultiplier: 1.1
};

const simA = new CookieRunSimulator(baseConfig);
const resA = simA.run();

const simB = new CookieRunSimulator({
  ...baseConfig,
  crashTimestamps: [35.0, 70.0]
});
const resB = simB.run();

console.log("Cookie Run Classic Simulation Comparison");
console.log("=========================================");
console.log("| Metric    | Perfect Run | 2 Crashes   | Diff      |");
console.log("|-----------|-------------|-------------|-----------|");

const metrics = [
  { label: "Score", key: "score" },
  { label: "Coins", key: "coins" },
  { label: "XP", key: "xp" },
  { label: "Time", key: "duration" }
];

metrics.forEach(m => {
  const valA = (resA as any)[m.key];
  const valB = (resB as any)[m.key];
  const diff = valA - valB;
  const pA = valA.toLocaleString().padEnd(11);
  const pB = valB.toLocaleString().padEnd(11);
  const pD = diff.toLocaleString().padEnd(9);
  console.log(`| ${m.label.padEnd(9)} | ${pA} | ${pB} | -${pD} |`);
});
console.log("=========================================");
