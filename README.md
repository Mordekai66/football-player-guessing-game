# Football Player Guessing Game

An intelligent AI-powered game that guesses which you're thinking of using **Information Theory** and **Decision Tree** concepts.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Current Scope

**Important Note**: The current player database is **limited to Premier League players only** for the **current season (2025-2026)**.

### Future Plans:
- **Add retired legends** (historical players)
- **Expand to Top 5 European leagues**:
  - Premier League (England)
  - La Liga (Spain)
  - Serie A (Italy)
  - Bundesliga (Germany)
  - Ligue 1 (France)
- **Include women's football players**
- **Add more player attributes** (age, market value, trophies, etc.)

### Current Focus:
The game currently specializes in identifying **active Premier League players** with high accuracy.

## Features

- **AI-Powered Guessing**: Uses Information Gain algorithm to ask optimal questions
- **Premier League Database**: Focused on current Premier League players
- **Smart Question Selection**: Always asks the most informative question
- **Probability Tracking**: Shows real-time probability distributions
- **User-Friendly Interface**: Interactive command-line interface
- **Error Resilient**: Robust error handling and data validation
- **Easy Expansion**: Modular design for adding more leagues and players

## How It Works

The game uses **Information Theory** concepts:
1. **Entropy Calculation**: Measures uncertainty in player selection
2. **Information Gain**: Determines which question reduces uncertainty the most
3. **Optimal Questioning**: Selects questions that maximize information gain
4. **Probability Updates**: Bayesian updating of player probabilities

### Algorithm Overview:
```
Initial State → Calculate Entropy → Compute Information Gain for all attributes 
→ Select Best Question → Update Probabilities → Repeat until confident
```

## Installation

### Prerequisites
- Python 3.7 or higher

### Clone the Repository or download as a zip file

### Run Directly
```bash
python main.py
```

## Project Structure

```
football-player-guessing-game/
├── main.py              # Main game engine
├── players.csv          # Premier League player database
└──  README.md           # This file
```

## Player Database Format

The `players.csv` file contains **current Premier League players** with these columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `name` | string | Player's full name | "Erling Haaland" |
| `club` | string | Premier League club | "Manchester City" |
| `position` | string | Playing position | "Forward" |
| `nationality` | string | Nationality | "Norway" |
| `retired` | boolean | Is retired? (false for all) | false |
| `ballon_dor` | boolean | Has won Ballon d'Or? | false |
| `champions_league` | boolean | Has won Champions League? | true |

### Example `players.csv` Entry:
```csv
name,club,position,nationality,retired,ballon_dor,champions_league
Mohamed Salah,Liverpool,Forward,Egypt,false,false,true
Bukayo Saka,Arsenal,Forward,England,false,false,false
Christopher Nkunku,Chelsea,Forward,France,false,false,false
Bruno Guimaraes,Newcastle United,false,Midfielder,Brazil,false,false
```

**Note**: Some players like Harry Kane have moved but are included for completeness.

## How to Play

1. **Start the game**:
   ```bash
   python main.py
   ```

2. **Think of a Premier League player** from the current season

3. **Answer questions** truthfully:
   - For yes/no questions: answer "yes" or "no"
   - For categorical questions: enter the specific value

4. **Watch as the AI** narrows down possibilities with each question

5. **The game ends** when:
   - The AI identifies the player with high confidence
   - Maximum questions (20) are reached
   - Only one player remains

## Premier League Clubs Covered

- Arsenal
- Aston Villa
- Bournemouth
- Brentford
- Brighton & Hove Albion
- Burnley
- Chelsea
- Crystal Palace
- Everton
- Fulham
- Liverpool
- Sunderland
- Manchester City
- Manchester United
- Newcastle United
- Nottingham Forest
- Leedz United
- Tottenham Hotspur
- West Ham United
- Wolverhampton Wanderers

## Usage Example

```text
============================================================
Welcome to the Player Guessing Engine!
============================================================
Current database: Premier League 2025-2026 Players

Loaded 520 player(s) to start!

============================================================
Question: 1
Remaining players: 520

Question: Does the player play for club?
Available options: Arsenal, Aston Villa, Bournemouth, Brentford, ...

Answer: Manchester City

==================================================
Possible Players:
==================================================
1. Erling Haaland (Manchester City, Forward, Norway)
   Probability: 5.3%
2. Kevin De Bruyne (Manchester City, Midfielder, Belgium)
   Probability: 5.3%
3. Phil Foden (Manchester City, Midfielder, England)
   Probability: 5.3%
... 15 more Manchester City players

... continues until player is identified ...
```

## Customization for Future Expansion

### To Add Retired Players:
```python
# In the CSV, set retired=True and include historical clubs
"Thierry Henry,Arsenal,Forward,France,true,false,true"
```

### To Add Other Leagues:
1. Add league column to CSV:
   ```csv
   name,club,league,position,nationality,retired,ballon_dor,champions_league
   "Lionel Messi,Inter Miami,MLS,Forward,Argentina,false,true,true"
   ```

2. Update ATTRIBUTES list:
   ```python
   ATTRIBUTES = [
       "league",  # New attribute
       "club",
       "position",
       # ... rest
   ]
   ```

## Performance with Premier League Data

The algorithm is optimized for Premier League characteristics:
- **Large squads**: 20 teams × ~25 players = ~500 players
- **Diverse nationalities**: Players from 60+ countries
- **Position variety**: GK, DEF, MID, FWD distributions
- **Trophy history**: CL winners, Ballon d'Or contenders

**Average game length**: 7-12 questions to identify any Premier League player.

## Data Sources:
- [Official Premier League Website](https://www.premierleague.com/players)
- [Transfermarkt](https://www.transfermarkt.com/)
- [FBref](https://fbref.com/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Disclaimer**: This project is for educational purposes. Player data is based on publicly available information and may not be 100% accurate or complete.
