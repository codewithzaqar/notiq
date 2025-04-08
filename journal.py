from datetime import datetime
from storage import save_entries, load_entries

class Journal:
    def __init__(self):
        self.entries = load_entries() or []

    def add_entry(self, title, content):
        if not title or not content:
            print("Title and content cannot be empty!")
            return
        entry = {
            "title": title,
            "content": content,
            "timestamp": datetime.now().strftime("%Y=%m-%d %H:%M:%S")
        }
        self.entries.append(entry)
        if save_entries(self.entries):
            print("Entry added successfully!")
        else:
            print("Failed to save entry.")

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
        
    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            deleted_entry = self.entries.pop(index)
            if save_entries(self.entries):
                print(f"Deleted entry: {deleted_entry['title']}")
            else:
                print("Failed to delete entry - save error.")
        else:
            raise IndexError("Entry index out of range")
        
    def search_entries(self, search_term):
        found = False
        for i, entry in enumerate(self.entries, 1):
            if search_term.lower() in entry['title'].lower():
                print(f"\nEntry #{i}")
                print(f"Title: {entry['title']}")
                print(f"Date: {entry['timestamp']}")
                print(f"Content: {entry['content']}")
                print("-" * 30)
                found = True
        if not found:
            print(f"No entries found containing '{search_term}'")