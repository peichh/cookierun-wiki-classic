# CookieRun Readable Database Project

## Project Status: Thursday, July 2, 2026

Current focus is on building a comprehensive, human-readable database and simulation environment for CookieRun. The project has successfully extracted and organized core game data, including assets, unit levels, and basic balance configurations.

### Recent Progress
- **Asset Extraction:** Multiple iterations of asset extraction (`v3`, `v4`, `v5`) have been completed.
- **Database Foundation:** Initial SQLite database (`cookierun_classic.db`) and JSON snapshots are in place.
- **Mechanism Mapping:** Preliminary work on magnetic ranges and game mechanics is underway.

---

## Open Loops & Next Steps

### 1. Lotus Root + Dancheong Simulator Setup
- Establish the core simulation logic for the Lotus Root cookie.
- Implement the Dancheong (Traditional Korean Pattern) mechanic logic within the simulator.

### 2. Hitbox Parsing (unit_balance)
- Extract and parse precise hitbox data from the `unit_balance` files.
- Integrate these hitboxes into the simulator for accurate collision detection.

### 3. Global Offset Multipliers
- Identify and apply global multipliers that affect distance and score offsets.
- Ensure parity with in-game physics and scoring.

### 4. Pet & Treasure Scaling
- Implement level-based scaling for Pet and Treasure stats.
- Map the progression curves to accurately reflect power levels.

### 5. Database Refinement
- Clean and normalize JSON data (e.g., removing redundant fields).
- Finalize the schema for the unified readable database.

### 6. Magnetic Aura Logic
- Refine the implementation of Magnetic Aura ranges using `magnetic_ranges.json`.
- Account for overlapping or stacked magnetic effects.

### 7. Combi Bonus Variable Logic
- Map the newly discovered variable logic structure for Combi Bonuses.
- Ensure the simulator correctly calculates bonuses based on specific Cookie/Pet/Treasure pairings.

---

## File Cleanup Recommendation
The following files are candidates for removal after verification:
- `database.zip`: Redundant if the `database/` directory is current.
- `extract_assets_v3.py`, `extract_assets_v4.py`: Superseded by `v5`.
- `fix_database_v3.py`: Likely an old migration script.
- `harvest_progress.log`: Temporary log file.
