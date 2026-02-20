
import glob
import os

def get_latest_processed_files():
    """
    Finds the most recent processed_matches CSV and tactical_report JSON files.
    """
    # This script assumes it is called from a context where the 'data' directory is a subdirectory.
    # Based on the project structure, this means running from 'FootballAnalyticsAI' or the root.
    
    # Search for files in all possible 'data/processed' directories to handle the nested structure
    base_paths = ['.', 'FootballAnalyticsAI']
    
    latest_csv = None
    latest_json = None
    latest_csv_mtime = 0
    latest_json_mtime = 0

    for base_path in base_paths:
        processed_dir = os.path.join(base_path, 'data', 'processed')
        
        # Find latest CSV
        csv_files = glob.glob(os.path.join(processed_dir, 'processed_matches_*.csv'))
        if csv_files:
            for f in csv_files:
                mtime = os.path.getmtime(f)
                if mtime > latest_csv_mtime:
                    latest_csv = f
                    latest_csv_mtime = mtime

        # Find tactical_report.json
        json_file = os.path.join(processed_dir, 'tactical_report.json')
        if os.path.exists(json_file):
             mtime = os.path.getmtime(json_file)
             if mtime > latest_json_mtime:
                latest_json = json_file
                latest_json_mtime = mtime


    return latest_csv, latest_json

if __name__ == '__main__':
    csv_file, json_file = get_latest_processed_files()
    print(f"Latest CSV: {csv_file}")
    print(f"Latest JSON: {json_file}")
