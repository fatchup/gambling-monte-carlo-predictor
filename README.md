# 🎲 Monte Carlo Parlay Simulator

A comprehensive tool to analyze sports parlay combinations, calculate Expected Value (EV), and determine if your bets are profitable using Monte Carlo simulations.

## Overview

This application allows you to:
- **Create custom parlay combinations** with any number of legs
- **Specify win probabilities** for each team in a matchup
- **Run Monte Carlo simulations** to estimate the true probability of each parlay combination
- **Calculate Expected Value (EV)** to determine if a bet is worth taking
- **Analyze financial outcomes** by showing total money won and lost for each combination
- **Compare all possible combinations** side-by-side sorted by profitability

## How It Works

### Parlay Combinations
A parlay is a single bet that combines multiple independent events. For a parlay to win, **ALL selected teams/events must win**. If even one loses, the entire bet is lost.

Example: 3-leg parlay with Red, Green, and Blue teams
- If all three win: You receive your bet × multiplier (e.g., $100 × 6.0 = $600)
- If any one loses: You lose your entire bet ($100)

### Monte Carlo Simulations
The application runs thousands of simulations for each possible parlay combination to estimate real-world outcomes. Each simulation represents one bet cycle where:
1. Each team's outcome is determined based on its win probability
2. The bet either wins (all teams win) or loses (any team loses)
3. Results are tracked across all simulations

### Expected Value (EV) Formula

The Expected Value formula determines the average profit or loss per dollar bet:

$$EV = P(\text{win}) \times \text{(profit if win)} + P(\text{loss}) \times \text{(profit if lose)}$$

Where:
- **P(win)** = Probability of winning the parlay (all teams win)
- **Profit if win** = (Multiplier - 1) × Bet Amount
- **P(loss)** = 1 - P(win) = Probability of losing the parlay
- **Profit if lose** = -Bet Amount

**Example:** For a 3-leg parlay with probabilities 50%, 50%, 50% and a 6.0x multiplier:
- P(win) = 0.5 × 0.5 × 0.5 = 0.125 (12.5%)
- P(loss) = 0.875 (87.5%)
- EV = 0.125 × (6.0 - 1) × $100 + 0.875 × (-$100)
- EV = 0.125 × $500 - $87.50 = $62.50 - $87.50 = **-$0.25 per $1 bet**

This means on average, you lose $0.25 for every $1 wagered.

### Interpreting Results

- **Positive EV**: Expected profit over many bets (good bet)
- **Negative EV**: Expected loss over many bets (bad bet from a statistical perspective)
- **EV = 0**: Break-even (fair bet)

## Features

✅ Configure any number of parlay legs  
✅ Auto-generate team names with random colors if left blank  
✅ Default to 0.5 probability for each team (50/50 odds)  
✅ Set custom bet amounts  
✅ Run large-scale simulations (100,000+ trials per combination)  
✅ View all possible combinations ranked by profitability  
✅ See detailed statistics: wins, losses, win rate, EV  
✅ Calculate total money won and lost for each combination  
✅ Beautiful GUI with real-time results  

## Usage

1. **Configure Teams**: Enter the number of parlay legs and team names/probabilities
   - Leave blank for auto-generated color names and 0.5 default probability
2. **Set Parameters**: 
   - Total multiplier for winning the parlay
   - Number of simulations to run
   - Bet amount per simulation
3. **Run Simulation**: Click "Run Simulation" to analyze all combinations
4. **Review Results**: See wins/losses, EV, and profitability for each combination

## Files

- `parlay_simulator_gui.py` - Main GUI application
- `monte_carlo.py` - Command-line version of the simulator

## Requirements

- Python 3.x
- tkinter (usually included with Python)

## Running the Application

### Option 1: Python Source (All Platforms)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python parlay_simulator_gui.py
```

### Option 2: macOS Executable

1. **Clone the repository**:
```bash
git clone https://github.com/fatchup/gambling-monte-carlo-predictor.git
cd gambling-monte-carlo-predictor
```

2. **Build the macOS app**:
```bash
bash build_mac.sh
```

3. **Run the app**:
```bash
open dist/Parlay\ Simulator.app
```

Or double-click `Parlay Simulator.app` in Finder.

### Option 3: Windows Executable

Download the pre-built `.exe` from the `dist/` folder and double-click to run, or build it yourself:

```bash
bash build_windows.sh
```

Then run: `dist/Parlay Simulator.exe`

## Building for Different Platforms

The `Parlay Simulator.spec` file is configured to work on both macOS and Windows. To build:

**On macOS:**
```bash
bash build_mac.sh
```

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pyinstaller
pyinstaller "Parlay Simulator.spec"
```

The output will be in the `dist/` folder.