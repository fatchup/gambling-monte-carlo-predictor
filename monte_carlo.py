import random

def simulate_parlay(teams_odds, multiplier, num_simulations):
    """
    Simulate a parlay with given team odds and multiplier.
    
    teams_odds: dict with team names as keys and win probability as values
    multiplier: total payout multiplier if all teams win
    num_simulations: number of simulations to run
    
    Returns: (wins, losses, ev_per_bet, total_ev)
    """
    stake = 1.0  # normalize to $1 bet
    wins = 0
    losses = 0
    total_profit = 0.0
    
    for _ in range(num_simulations):
        # Check if all teams win this simulation
        all_win = True
        for team, probability in teams_odds.items():
            if random.random() > probability:
                all_win = False
                break
        
        if all_win:
            # Win: get multiplier times stake
            profit = stake * multiplier - stake
            total_profit += profit
            wins += 1
        else:
            # Loss: lose the stake
            total_profit -= stake
            losses += 1
    
    ev_per_bet = total_profit / num_simulations
    total_ev = total_profit
    
    return wins, losses, ev_per_bet, total_ev

def run():
    print("\n--- Monte Carlo Parlay Simulator with EV Calculator ---\n")
    
    # Get number of parlays (legs in the parlay)
    num_parlays = int(input("How many parlays (legs) are there? (e.g., 3 for 3-leg parlay): ").strip())
    
    # Get team names and odds for each parlay
    teams_odds = {}
    print(f"\nEnter team names and their win probability for each of the {num_parlays} matchups:")
    print("(Each matchup is 1v1, so you'll enter 2 team names per matchup)\n")
    
    for i in range(num_parlays):
        print(f"Matchup {i+1}:")
        team1_name = input(f"  Team 1 name: ").strip()
        team1_odds = float(input(f"  {team1_name} win probability (0-1): ").strip())
        
        team2_name = input(f"  Team 2 name: ").strip()
        team2_odds = float(input(f"  {team2_name} win probability (0-1): ").strip())
        
        # For the parlay, we need to pick one team per matchup
        # The user should input the probability of the team they're betting on winning
        if team1_odds >= team2_odds:
            teams_odds[team1_name] = team1_odds
            print(f"  → Picking {team1_name} with {team1_odds*100:.1f}% win probability\n")
        else:
            teams_odds[team2_name] = team2_odds
            print(f"  → Picking {team2_name} with {team2_odds*100:.1f}% win probability\n")
    
    # Get total multiplier
    multiplier = float(input("What is the total multiplier if you win the parlay? (e.g., 8.5): ").strip())
    
    # Get number of simulations
    num_simulations = int(input("How many simulations would you like to run? (e.g., 100000): ").strip())
    
    print("\n--- Running simulations ---")
    random.seed()
    
    wins, losses, ev_per_bet, total_ev = simulate_parlay(teams_odds, multiplier, num_simulations)
    
    # Calculate theoretical probability of winning
    theoretical_win_prob = 1.0
    for team, prob in teams_odds.items():
        theoretical_win_prob *= prob
    
    theoretical_loss_prob = 1.0 - theoretical_win_prob
    
    # Calculate theoretical EV
    win_payout = multiplier - 1  # profit if win (normalized to $1 bet)
    loss_payout = -1.0  # loss if lose
    theoretical_ev = (theoretical_win_prob * win_payout) + (theoretical_loss_prob * loss_payout)
    
    # Display results
    print("\n" + "="*60)
    print("--- RESULTS ---")
    print("="*60)
    
    print("\n--- Teams and Odds ---")
    for i, (team, prob) in enumerate(teams_odds.items(), 1):
        print(f"  {i}. {team}: {prob*100:.2f}%")
    
    print(f"\nParlay Multiplier: {multiplier}x")
    print(f"Simulations Run: {num_simulations:,}")
    
    print("\n--- Simulation Results ---")
    print(f"  Wins: {wins:,}")
    print(f"  Losses: {losses:,}")
    print(f"  Win Rate: {(wins/num_simulations)*100:.2f}%")
    
    print("\n--- Expected Value (EV) ---")
    print(f"  EV per $1 bet: ${ev_per_bet:.4f}")
    print(f"  Theoretical EV per $1 bet: ${theoretical_ev:.4f}")
    print(f"  Probability of Winning (Simulated): {(wins/num_simulations)*100:.2f}%")
    print(f"  Probability of Winning (Theoretical): {theoretical_win_prob*100:.2f}%")
    
    if ev_per_bet < 0:
        print(f"\n  ⚠ This is a NEGATIVE EV bet (expected loss of ${abs(ev_per_bet):.4f} per $1 bet)")
    else:
        print(f"\n  ✓ This is a POSITIVE EV bet (expected gain of ${ev_per_bet:.4f} per $1 bet)")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    run()
