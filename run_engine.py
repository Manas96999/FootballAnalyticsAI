import os
import sys
import json
import pandas as pd

# --- Setup Python Path ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'python')))

# --- Import Engine Components ---
try:
    from preprocess import load_latest_raw_data, preprocess_data
    from archiver import archive_match_summary
except ImportError as e:
    print(f"Error: A required module was not found. Details: {e}")
    sys.exit(1)

def run_engine():
    """
    Executes the full data processing and archiving pipeline.
    """
    print("--- [WORKFLOW START] ---")

    # 1. Data Preprocessing
    print("\n[Step 1/3] Running Data Preprocessing...")
    raw_data = load_latest_raw_data()
    if raw_data:
        processed_df, _ = preprocess_data(raw_data)
        if processed_df is not None:
            print("[SUCCESS] Data Preprocessing complete.")

            # 2. Data Archiving
            print("\n[Step 2/3] Running Data Archiving...")
            
            json_path = 'dataset/processed/tactical_report.json'
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    tactical_reports = json.load(f)

                for _, row in processed_df.iterrows():
                    match_data = row.to_dict()
                    report = next((r for r in tactical_reports if r.get('match') and r['match'] in f"{match_data.get('home_team')} vs {match_data.get('away_team')}"), None)
                    
                    if report:
                        archive_match_summary(match_data, report.get('tactical_observation', 'No insight available.'))
                print("[SUCCESS] Data Archiving complete.")
            else:
                print("[WARNING] Archiving skipped: tactical_report.json not found.")
        else:
            print("[ERROR] Preprocessing failed. Halting workflow.")
    else:
        print("[ERROR] No raw data found. Halting workflow.")

    print("\n--- [WORKFLOW FINISHED] ---")

if __name__ == '__main__':
    run_engine()
