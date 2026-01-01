import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from tkinter import font
from itertools import product

class ParlaySimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monte Carlo Parlay Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Set style
        self.setup_styles()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Title
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        title_label = tk.Label(main_frame, text="🎲 Monte Carlo Parlay Simulator", 
                               font=title_font, bg="#f0f0f0", fg="#333")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Parlay Configuration", padding="15")
        input_frame.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        
        # Number of parlays
        ttk.Label(input_frame, text="Number of Parlays (Legs):").grid(row=0, column=0, sticky="w", pady=5)
        self.num_parlays_var = tk.StringVar(value="3")
        ttk.Spinbox(input_frame, from_=1, to=10, textvariable=self.num_parlays_var, width=10).grid(row=0, column=1, sticky="w", pady=5)
        
        # Multiplier
        ttk.Label(input_frame, text="Total Multiplier (if win):").grid(row=1, column=0, sticky="w", pady=5)
        self.multiplier_var = tk.StringVar(value="8.5")
        ttk.Entry(input_frame, textvariable=self.multiplier_var, width=10).grid(row=1, column=1, sticky="w", pady=5)
        
        # Simulations
        ttk.Label(input_frame, text="Number of Simulations:").grid(row=2, column=0, sticky="w", pady=5)
        self.simulations_var = tk.StringVar(value="100000")
        ttk.Entry(input_frame, textvariable=self.simulations_var, width=10).grid(row=2, column=1, sticky="w", pady=5)
        
        # Bet Amount
        ttk.Label(input_frame, text="Bet Amount per Simulation ($):").grid(row=3, column=0, sticky="w", pady=5)
        self.bet_amount_var = tk.StringVar(value="100")
        ttk.Entry(input_frame, textvariable=self.bet_amount_var, width=10).grid(row=3, column=1, sticky="w", pady=5)
        
        # Button to add teams
        ttk.Button(input_frame, text="Configure Teams", command=self.open_teams_window).grid(row=4, column=0, columnspan=2, pady=15, sticky="ew")
        
        # Teams display
        ttk.Label(input_frame, text="Teams:").grid(row=5, column=0, sticky="w", pady=(10, 5))
        self.teams_display = scrolledtext.ScrolledText(input_frame, height=6, width=40, state="disabled")
        self.teams_display.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Simulate button
        ttk.Button(input_frame, text="▶ Run Simulation", command=self.run_simulation).grid(row=7, column=0, columnspan=2, pady=15, sticky="ew")
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="15")
        results_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Results display
        self.results_display = scrolledtext.ScrolledText(results_frame, height=30, width=50, 
                                                         state="disabled", font=("Courier", 9))
        self.results_display.grid(row=0, column=0, sticky="nsew")
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.teams_odds = {}
        self.all_matchups = {}  # Store all teams for each matchup
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        style.configure('TLabelFrame', background='#f0f0f0', font=('Helvetica', 10, 'bold'))
        style.configure('TEntry', font=('Helvetica', 10))
        style.configure('TSpinbox', font=('Helvetica', 10))
    
    def open_teams_window(self):
        try:
            num_parlays = int(self.num_parlays_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of parlays")
            return
        
        teams_window = tk.Toplevel(self.root)
        teams_window.title("Configure Teams")
        teams_window.geometry("500x400")
        teams_window.configure(bg="#f0f0f0")
        
        frame = ttk.Frame(teams_window, padding="15")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text=f"Enter team names and win probabilities for {num_parlays} matchups\n(Leave blank for random color and 0.5 probability)").pack(pady=10)
        
        canvas = tk.Canvas(frame, bg="white", highlightthickness=1, highlightbackground="#ddd")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding="10")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.team_entries = []
        
        for i in range(num_parlays):
            matchup_frame = ttk.LabelFrame(scrollable_frame, text=f"Matchup {i+1}", padding="10")
            matchup_frame.pack(fill="x", pady=5)
            
            ttk.Label(matchup_frame, text="Team 1 Name:").grid(row=0, column=0, sticky="w")
            team1_name = ttk.Entry(matchup_frame, width=20)
            team1_name.grid(row=0, column=1, sticky="ew", padx=5)
            
            ttk.Label(matchup_frame, text="Win Probability (0-1):").grid(row=1, column=0, sticky="w")
            team1_prob = ttk.Entry(matchup_frame, width=20)
            team1_prob.grid(row=1, column=1, sticky="ew", padx=5)
            
            ttk.Label(matchup_frame, text="Team 2 Name:").grid(row=2, column=0, sticky="w")
            team2_name = ttk.Entry(matchup_frame, width=20)
            team2_name.grid(row=2, column=1, sticky="ew", padx=5)
            
            ttk.Label(matchup_frame, text="Win Probability (0-1):").grid(row=3, column=0, sticky="w")
            team2_prob = ttk.Entry(matchup_frame, width=20)
            team2_prob.grid(row=3, column=1, sticky="ew", padx=5)
            
            matchup_frame.columnconfigure(1, weight=1)
            
            self.team_entries.append({
                'team1_name': team1_name,
                'team1_prob': team1_prob,
                'team2_name': team2_name,
                'team2_prob': team2_prob
            })
        
        def save_teams():
            try:
                self.teams_odds = {}
                self.all_matchups = {}
                used_colors = set()
                
                colors = ["Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Cyan", 
                         "Magenta", "Lime", "Indigo", "Violet", "Turquoise", "Gold", "Silver",
                         "Maroon", "Navy", "Teal", "Olive", "Coral", "Salmon", "Khaki", "Plum"]
                
                color_index = 0
                
                for i, entry in enumerate(self.team_entries):
                    t1_name = entry['team1_name'].get().strip()
                    t1_prob_str = entry['team1_prob'].get().strip()
                    t2_name = entry['team2_name'].get().strip()
                    t2_prob_str = entry['team2_prob'].get().strip()
                    
                    # Assign default values if empty
                    if not t1_name:
                        while color_index < len(colors) and colors[color_index] in used_colors:
                            color_index += 1
                        if color_index < len(colors):
                            t1_name = colors[color_index]
                            used_colors.add(t1_name)
                            color_index += 1
                        else:
                            messagebox.showerror("Error", "Too many teams, ran out of colors!")
                            return
                    
                    if not t1_prob_str:
                        t1_prob = 0.5
                    else:
                        t1_prob = float(t1_prob_str)
                    
                    if not t2_name:
                        while color_index < len(colors) and colors[color_index] in used_colors:
                            color_index += 1
                        if color_index < len(colors):
                            t2_name = colors[color_index]
                            used_colors.add(t2_name)
                            color_index += 1
                        else:
                            messagebox.showerror("Error", "Too many teams, ran out of colors!")
                            return
                    
                    if not t2_prob_str:
                        t2_prob = 0.5
                    else:
                        t2_prob = float(t2_prob_str)
                    
                    if not (0 <= t1_prob <= 1) or not (0 <= t2_prob <= 1):
                        messagebox.showerror("Invalid Input", "Probabilities must be between 0 and 1")
                        return
                    
                    # Store all teams for this matchup
                    self.all_matchups[i] = {
                        t1_name: t1_prob,
                        t2_name: t2_prob
                    }
                    
                    # Pick the team with higher probability for default
                    if t1_prob >= t2_prob:
                        self.teams_odds[t1_name] = t1_prob
                    else:
                        self.teams_odds[t2_name] = t2_prob
                
                self.update_teams_display()
                teams_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for probabilities")
        
        ttk.Button(frame, text="Save Teams", command=save_teams).pack(pady=10, fill="x")
    
    def update_teams_display(self):
        self.teams_display.config(state="normal")
        self.teams_display.delete(1.0, tk.END)
        
        if self.teams_odds:
            for i, (team, prob) in enumerate(self.teams_odds.items(), 1):
                self.teams_display.insert(tk.END, f"{i}. {team}: {prob*100:.2f}%\n")
        else:
            self.teams_display.insert(tk.END, "No teams configured yet")
        
        self.teams_display.config(state="disabled")
    
    def run_simulation(self):
        try:
            if not self.all_matchups:
                messagebox.showerror("Error", "Please configure teams first")
                return
            
            multiplier = float(self.multiplier_var.get())
            num_simulations = int(self.simulations_var.get())
            bet_amount = float(self.bet_amount_var.get())
            
            if multiplier <= 0 or num_simulations <= 0 or bet_amount <= 0:
                messagebox.showerror("Invalid Input", "Multiplier, simulations, and bet amount must be positive")
                return
            
            # Generate all possible combinations
            matchup_lists = [list(self.all_matchups[i].items()) for i in sorted(self.all_matchups.keys())]
            all_combinations = list(product(*matchup_lists))
            
            # Run simulations for all combinations
            results = self.simulate_all_combinations(matchup_lists, all_combinations, multiplier, num_simulations)
            
            # Display results
            self.display_all_results(results, multiplier, num_simulations, bet_amount)
        
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers")
    
    def simulate_all_combinations(self, matchup_lists, all_combinations, multiplier, num_simulations):
        results = []
        
        for combo in all_combinations:
            teams_odds = {team: prob for team, prob in combo}
            wins, losses, ev_per_bet, theoretical_win_prob = self.simulate_parlay(
                teams_odds, multiplier, num_simulations
            )
            
            results.append({
                'teams': teams_odds,
                'wins': wins,
                'losses': losses,
                'ev_per_bet': ev_per_bet,
                'theoretical_prob': theoretical_win_prob
            })
        
        return results
    
    def simulate_parlay(self, teams_odds, multiplier, num_simulations):
        stake = 1.0
        wins = 0
        
        random.seed()
        
        for _ in range(num_simulations):
            all_win = True
            for team, probability in teams_odds.items():
                if random.random() > probability:
                    all_win = False
                    break
            
            if all_win:
                wins += 1
        
        losses = num_simulations - wins
        
        # Calculate theoretical probability
        theoretical_win_prob = 1.0
        for team, prob in teams_odds.items():
            theoretical_win_prob *= prob
        
        theoretical_loss_prob = 1.0 - theoretical_win_prob
        win_payout = multiplier - 1
        loss_payout = -1.0
        ev_per_bet = (theoretical_win_prob * win_payout) + (theoretical_loss_prob * loss_payout)
        
        return wins, losses, ev_per_bet, theoretical_win_prob
    
    def display_all_results(self, results, multiplier, num_simulations, bet_amount):
        self.results_display.config(state="normal")
        self.results_display.delete(1.0, tk.END)
        
        results_text = f"""
╔════════════════════════════════════════╗
║        ALL PARLAY COMBINATIONS         ║
╚════════════════════════════════════════╝

📊 SIMULATION SETTINGS:
  Multiplier: {multiplier}x
  Total Simulations per Combination: {num_simulations:,}
  Bet Amount per Simulation: ${bet_amount:.2f}
  Total Combinations: {len(results)}

"""
        
        # Sort by EV (best to worst)
        sorted_results = sorted(results, key=lambda x: x['ev_per_bet'], reverse=True)
        
        for idx, result in enumerate(sorted_results, 1):
            combination_str = " + ".join(result['teams'].keys())
            win_rate = (result['wins'] / (result['wins'] + result['losses'])) * 100
            theoretical_prob_pct = result['theoretical_prob'] * 100
            
            # Calculate money won and lost
            money_won = result['wins'] * bet_amount * (multiplier - 1)
            money_lost = result['losses'] * bet_amount
            net_profit = money_won - money_lost
            
            results_text += f"{'='*60}\n"
            results_text += f"#{idx}: {combination_str}\n"
            results_text += f"{'='*60}\n"
            results_text += f"  Probabilities: {', '.join([f'{prob*100:.2f}%' for prob in result['teams'].values()])}\n"
            results_text += f"  Theoretical Chance: {theoretical_prob_pct:.4f}%\n"
            results_text += f"  Simulated Wins: {result['wins']:,}\n"
            results_text += f"  Simulated Losses: {result['losses']:,}\n"
            results_text += f"  Simulated Win Rate: {win_rate:.4f}%\n"
            results_text += f"  EV per $1 bet: ${result['ev_per_bet']:.4f}\n\n"
            
            results_text += f"💰 MONEY CONCLUSION:\n"
            results_text += f"  Money Won (Wins):    ${money_won:,.2f}\n"
            results_text += f"  Money Lost (Losses): ${money_lost:,.2f}\n"
            
            if net_profit >= 0:
                results_text += f"  ✓ NET PROFIT:        ${net_profit:,.2f}\n"
            else:
                results_text += f"  ⚠️  NET LOSS:         ${net_profit:,.2f}\n"
            results_text += "\n"
        
        self.results_display.insert(tk.END, results_text)
        self.results_display.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ParlaySimulatorApp(root)
    root.mainloop()
