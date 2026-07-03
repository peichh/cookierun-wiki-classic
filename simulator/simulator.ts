import { PlayerStats, SimConfig, SimulationResult } from './types';

export class CookieRunSimulator {
  private BASE_SPEED = 300;
  private BASE_DRAIN = 3.0; // Character_EnergyDiminishValueNew
  private CRASH_DAMAGE = 40;
  private ROLLING_TIME = 1.0;
  private IMMORTAL_TIME = 2.0;
  
  private currentHp: number;
  private currentScore = 0;
  private totalCoins = 0;
  private totalXp = 0;
  private currentTime = 0;
  private distance = 0;
  
  private immortalUntil = 0;
  private speedRestoreAt = 0;
  
  private isQuickStarting = false;
  private quickStartEnd = 0;
  
  private bonusTimes = [60, 150]; // Hardcoded trigger times for sim
  private inBonusTime = false;
  private bonusTimeEnd = 0;

  constructor(private config: SimConfig) {
    // Calc Initial HP: Base 100 + 2 per Heart Level
    this.currentHp = 100 + (config.player.heartLevel * 2);
    
    if (config.boosters.includes('Health Boost')) {
      this.currentHp += 30;
    }
  }

  public run(): SimulationResult {
    const timeStep = 0.1; // 100ms precision
    
    if (this.config.boosters.includes('Quick Start')) {
      this.isQuickStarting = true;
      this.quickStartEnd = 15.0;
    }

    while (this.currentHp > 0) {
      this.step(timeStep);
      this.currentTime += timeStep;
      
      // Stop safety
      if (this.currentTime > 600) break; 
    }

    // Apply User Level Bonus
    // Level 100 -> 5.4x multiplier
    const userBonus = 1 + (this.config.player.userLevel * 0.044); // Simplified linear scale
    const finalScore = Math.floor(this.currentScore * userBonus);
    
    if (this.config.boosters.includes('Double XP')) {
      this.totalXp *= 2;
    }

    return {
      score: finalScore,
      coins: Math.floor(this.totalCoins),
      xp: Math.floor(this.totalXp),
      distance: Math.floor(this.distance),
      duration: Math.floor(this.currentTime)
    };
  }

  private step(dt: number) {
    // 1. Determine State
    const isCrashing = this.currentTime < this.speedRestoreAt;
    
    // Check for new Crash
    const scheduledCrash = this.config.crashTimestamps.find(t => 
      Math.abs(t - this.currentTime) < (dt / 2)
    );
    
    if (scheduledCrash && this.currentTime >= this.immortalUntil) {
      this.currentHp -= this.CRASH_DAMAGE;
      this.speedRestoreAt = this.currentTime + this.ROLLING_TIME;
      this.immortalUntil = this.currentTime + this.IMMORTAL_TIME;
    }

    // Bonus Time Trigger
    if (!this.inBonusTime && this.bonusTimes.some(bt => Math.abs(bt - this.currentTime) < (dt / 2))) {
       this.inBonusTime = true;
       // 7s + 0.1s * Bonus Level
       const duration = 7 + (this.config.player.bonusTimeLevel * 0.1);
       this.bonusTimeEnd = this.currentTime + duration;
    }

    if (this.inBonusTime && this.currentTime >= this.bonusTimeEnd) {
      this.inBonusTime = false;
    }

    // 2. Physics & Energy
    let currentSpeed = this.BASE_SPEED;
    if (this.isQuickStarting && this.currentTime < this.quickStartEnd) {
      currentSpeed = 600;
    } else if (this.config.randomBoost === '+17% speed') {
      currentSpeed *= 1.17;
    }

    if (isCrashing) {
      currentSpeed *= 0.5;
    }

    if (!this.inBonusTime) {
      let drainRate = this.BASE_DRAIN * this.config.episodeMultiplier;
      if (this.config.randomBoost === '-15% HP drain') {
        drainRate *= 0.85;
      }
      this.currentHp -= drainRate * dt;
    }

    this.distance += currentSpeed * dt;

    // 3. Scoring (Simplified Spawn Rates)
    // Assume 1 Jelly every 10 units, 1 Bear every 50 units, 1 Coin every 30 units
    const jellyScore = (1000 + this.config.player.jellyLevel * 100);
    
    this.currentScore += (currentSpeed * dt / 10) * jellyScore;
    this.currentScore += (currentSpeed * dt / 50) * 2600; // Bear
    
    this.totalCoins += (currentSpeed * dt / 30);
    this.totalXp += 10 * dt;
  }
}
