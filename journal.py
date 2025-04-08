from datetime import datetime
from storage import save_entries, load_entries

class Journal:
    def __init__(self):
        self.entries = load_entries() or []

    def add_entry(self, title, content):
        entry = {
            "title": title,
            "content": content,
            "timestamp": datetime.now().strftime("%Y=%m-%d %H:%M:%S")
        }
        self.entries.append(entry)
        save_entries(self.entries)
        print("Entry added successfully!")

    def view_entries(self):
        if not self.entries:
            print("No entries found.")
            return
        
        for i, entry in enumerate(self.entries, 1):
            print(f"\nEntry #{i}")
            print(f"Title: {entry['title']}")
            print(f"Date: {entry['timestamp']}")
            print(f"Content: {entry['content']}")
            print("-" * 30)