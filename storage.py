import json
import os

STORAGE_FILE = "journal_entries.json"

def save_entries(entries):
    try:
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(entries, f)
        return True
    except Exception as e:
        print(f"Error saving entries: {e}")
        return False

def load_entries():
    try:
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except json.JSONDecodeError as e:
        print(f"Error loading entries: Invalid JSON format - {str(e)}")
        return []
    except UnicodeDecodeError as e:
        print(f"Error loading entries: Encoding error - {str(e)}")
        return []
    except Exception as e:
        print(f"Error loading entries: {str(e)}")
        return []