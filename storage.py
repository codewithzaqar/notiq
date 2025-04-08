import json
import os

STORAGE_FILE = "journal_entries.json"

def save_entries(entries):
    try:
        with open(STORAGE_FILE, 'w') as f:
            json.dump(entries, f)
        return True
    except Exception as e:
        print(f"Error saving entries: {e}")
        return False
    
def load_entries():
    try:
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading entries: {e}")
        return []