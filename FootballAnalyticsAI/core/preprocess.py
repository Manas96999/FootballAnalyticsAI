import pandas as pd
import json
import os
from datetime import datetime
import glob
import numpy as np

def load_latest_raw_data(data_raw_dir='FootballAnalyticsAI/data/raw/'):
    """
    Loads the latest raw JSON match data from the specified directory.
    """
    list_of_files = glob.glob(os.path.join(data_raw_dir, '*.json'))
    if not list_of_files:
        print(f"No raw JSON files found in {data_raw_dir}")
        return None

    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Loading latest raw data from: {latest_file}")

    with open(latest_file, 'r') as f:
        raw_data = json.load(f)
    return raw_data

def preprocess_data(raw_data):
    """
    Processes the raw football match data.
    """
    if not raw_data:
        return None, None

    matches = raw_data.get('matches', [])
    if not matches:
        print("No matches found in the raw data.")
        return None, None

    df = pd.json_normalize(matches)

    df = df.rename(columns={
        'utcDate': 'date',
        'status': 'match_status',
        'homeTeam.name': 'home_team',
        'awayTeam.name': 'away_team',
        'score.fullTime.home': 'home_score',
        'score.fullTime.away': 'away_score',
        'competition.name': 'competition'
    })

    df['date'] = pd.to_datetime(df['date'])

    df_processed = df[[
        'date', 'competition', 'home_team', 'away_team',
        'home_score', 'away_score', 'match_status'
    ]].copy()

    df_processed['home_score'] = pd.to_numeric(df_processed['home_score'], errors='coerce').fillna(0).astype(int)
    df_processed['away_score'] = pd.to_numeric(df_processed['away_score'], errors='coerce').fillna(0).astype(int)

    # Add placeholder data for Radar Chart and xG
    df_processed['attacking'] = np.random.randint(60, 95, size=len(df_processed))
    df_processed['defensive'] = np.random.randint(60, 95, size=len(df_processed))
    df_processed['speed'] = np.random.randint(60, 95, size=len(df_processed))
    df_processed['discipline'] = np.random.randint(60, 95, size=len(df_processed))
    df_processed['possession'] = np.random.randint(40, 60, size=len(df_processed))
    df_processed['home_xG'] = np.round(np.random.uniform(0.5, 2.5, size=len(df_processed)), 2)
    df_processed['away_xG'] = np.round(np.random.uniform(0.5, 2.5, size=len(df_processed)), 2)

    prompt_data = []
    for index, row in df_processed.iterrows():
        prompt = (
            f"Match on {row['date'].strftime('%Y-%m-%d')}, Competition: {row['competition']}. "
            f"Home Team: {row['home_team']} (Score: {row['home_score']}), "
            f"Away Team: {row['away_team']} (Score: {row['away_score']}). "
            f"Match Status: {row['match_status']}. "
            f"Predict the outcome and provide tactical insights."
        )
        prompt_data.append(prompt)

    output_processed_dir = 'FootballAnalyticsAI/data/processed/'
    os.makedirs(output_processed_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    processed_csv_path = os.path.join(output_processed_dir, f'processed_matches_{timestamp}.csv')
    df_processed.to_csv(processed_csv_path, index=False)
    print(f"Saved processed match data to {processed_csv_path}")

    prompt_text_path = os.path.join(output_processed_dir, f'gemini_prompts_{timestamp}.txt')
    with open(prompt_text_path, 'w') as f:
        for p in prompt_data:
            f.write(p + "\n---\n")
    print(f"Saved Gemini prompt data to {prompt_text_path}")

    return df_processed, prompt_data

if __name__ == "__main__":
    raw_data = load_latest_raw_data()
    if raw_data:
        processed_df, gemini_prompts = preprocess_data(raw_data)
        if processed_df is not None:
            print("\nPreprocessing complete.")
            print(processed_df.head())
