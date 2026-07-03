export interface PlayerStats {
  hp: number;
  jellyLevel: number;
  bonusTimeLevel: number;
  userLevel: number;
  heartLevel: number;
}

export interface Booster {
  id: string;
  name: string;
  effect: any;
}

export interface SimConfig {
  player: PlayerStats;
  boosters: string[]; // ['Quick Start', 'Health Boost', etc.]
  randomBoost: string | null;
  crashTimestamps: number[];
  episodeMultiplier: number;
}

export interface SimulationResult {
  score: number;
  coins: number;
  xp: number;
  distance: number;
  duration: number;
}
