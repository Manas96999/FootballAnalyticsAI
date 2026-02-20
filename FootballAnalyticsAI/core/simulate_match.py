import time
import random
import pandas as pd
import json
import os
from datetime import datetime

# Setup paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
os.makedirs(DATA_DIR, exist_ok=True)

CSV_PATH = os.path.join(DATA_DIR, 'matches_data.csv')
JSON_PATH = os.path.join(DATA_DIR, 'tactical_report.json')

def generate_tactical_insight(minute, score_home, score_away, momentum):
    """Generates a realistic AI comment based on the match state."""
    if minute < 10:
        return "Match started. Both teams fighting for midfield control."
    
    if score_home > score_away:
        if momentum > 60:
            return f"Home team dominating possession ({momentum}%) and looking for a second goal."
        else:
            return "Home team sitting deep to protect the lead. Counter-attacking opportunities detected."
            
    elif score_away > score_home:
        return "Away team controlling the tempo. Home team struggling to break the defensive block."
    
    else: # Draw
        if minute > 80:
            return "High intensity! Both teams pushing for a late winner. Fatigue affecting defensive lines."
        return "Even contest. Midfield battle is key right now."

def simulate_match():
    print("🏟️  STARTING LIVE MATCH SIMULATION: Man City vs Arsenal")
    
    # Initial Stats
    home_score = 0
    away_score = 0
    home_xg = 0.0
    away_xg = 0.0
    possession = 50
    win_prob = 35 # Start with draw likelihood
    
    # Simulation Loop (1 to 90 minutes)
    for minute in range(1, 91):
        
        # 1. Simulate Events
        event = random.random()
        
        # Goal Chance (Low probability)
        if event < 0.03: 
            if random.random() > 0.5:
                home_score += 1
                home_xg += 0.45
                print(f"⚽ GOAL! Man City scores! ({minute}')")
            else:
                away_score += 1
                away_xg += 0.38
                print(f"⚽ GOAL! Arsenal scores! ({minute}')")
        
        # Shot Chance
        elif event < 0.15:
            if random.random() > 0.5:
                home_xg += random.uniform(0.05, 0.2)
            else:
                away_xg += random.uniform(0.05, 0.2)

        # Fluctuations
        possession += random.randint(-2, 2)
        possession = max(30, min(70, possession)) # Keep betwen 30-70%
        
        # Calculate Win Probability based on score
        if home_score > away_score:
            win_prob = min(95, win_prob + 2)
        elif away_score > home_score:
            win_prob = max(5, win_prob - 2)
        else:
            # Revert towards draw (33-33-33 split roughly)
            if win_prob > 50: win_prob -= 1
            if win_prob < 20: win_prob += 1
        
        # Radar metrics
        attacking = min(99, int(home_xg * 20))
        defensive = 100 - possession
        speed = random.randint(60, 90)
        discipline = random.randint(70, 95)

        # 2. Create Data Structure for CSV
        match_data = [{
            "home_team": "Man City",
            "away_team": "Arsenal",
            "home_score": home_score,
            "away_score": away_score,
            "match_time": f"{minute:02d}:{random.randint(0,59):02d}",
            "possession": possession,
            "home_xG": round(home_xg, 2),
            "away_xG": round(away_xg, 2),
            "attacking": attacking,
            "defensive": defensive,
            "speed": speed,
            "discipline": discipline
        }]

        # 3. Save CSV
        df = pd.DataFrame(match_data)
        df.to_csv(CSV_PATH, index=False)

        # 4. Generate & Save JSON Report
        insight = generate_tactical_insight(minute, home_score, away_score, possession)
        
        report_data = [{
            "tactical_observation": insight,
            "win_probability": {
                "home": win_prob,
                "draw": max(0, 100 - win_prob - (100-win_prob)/2), # Rough math for draw
                "away": max(0, (100-win_prob)/2)
            },
            "radar_metrics": {
                "attacking": attacking,
                "defensive": defensive,
                "possession": possession,
                "speed": speed,
                "discipline": discipline
            }
        }]
        
        with open(JSON_PATH, 'w') as f:
            json.dump(report_data, f)

        # Log to terminal
        print(f"⏱️ {minute}': {home_score}-{away_score} | xG: {home_xg:.2f}-{away_xg:.2f} | Insight: {insight}")
        
        # Wait 2 seconds before next update (Fast-forward mode)
        time.sleep(2)

    print("\n🏁 MATCH FINISHED")

if __name__ == "__main__":
    simulate_match()