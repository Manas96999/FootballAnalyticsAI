import os
from datetime import datetime

def archive_match_summary(match_data, tactical_insight):
    """
    Appends a summary of a match to the match_history.md file.

    Args:
        match_data (dict): A dictionary containing match data 
                           (e.g., home_team, away_team, home_score, away_score).
        tactical_insight (str): The AI-generated tactical observation for the match.
    """
    output_dir = os.path.join('dataset')
    os.makedirs(output_dir, exist_ok=True)
    history_file = os.path.join(output_dir, 'match_history.md')

    try:
        with open(history_file, 'a') as f:
            f.write(f"## {match_data.get('home_team', 'N/A')} vs {match_data.get('away_team', 'N/A')} - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"**Final Score:** {match_data.get('home_score', 'N/A')} - {match_data.get('away_score', 'N/A')}\n\n")
            f.write(f"**AI Tactical Observation:**\n")
            f.write(f"> {tactical_insight}\n\n")
            f.write("---\n\n")
        print(f"Successfully archived match summary to {history_file}")
    except Exception as e:
        print(f"Error archiving match summary: {e}")

if __name__ == '__main__':
    # This is an example of how to use the archiver.
    # In a real workflow, this would be called with actual data.
    print("Running archiver.py standalone for demonstration.")
    
    # Example Data
    example_match = {
        'home_team': 'FC Example',
        'away_team': 'Test United',
        'home_score': 3,
        'away_score': 1
    }
    example_insight = "FC Example dominated the midfield, leading to a comfortable victory."
    
    archive_match_summary(example_match, example_insight)
