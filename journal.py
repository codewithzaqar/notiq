from datetime import datetime
import json
import re
from storage import save_entries, load_entries

class Journal:
    def __init__(self):
        self.entries = load_entries() or []

    def add_entry(self, title, content, category=""):
        if not title or not content:
            print("Title and content cannot be empty!")
            return
        entry = {
            "title": title,
            "content": content,
            "category": category,
            "timestamp": datetime.now().strftime("%Y=%m-%d %H:%M:%S")
        }
        self.entries.append(entry)
        if save_entries(self.entries):
            print("Entry added successfully!")
        else:
            print("Failed to save entry.")

    def view_entries(self, sort_by="date", date_filter="", category_filter=""):
        if not self.entries:
            print("No entries found.")
            return
        
        filtered_entries = self.entries
        if date_filter:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_filter):
                print("Invalid date format. Use YYYY-MM-DD")
                return
            filtered_entries = [e for e in self.entries 
                                if e['timestamp'].startswith(date_filter)]
            if not filtered_entries:
                print(f"No entries found for {date_filter}")
                return
                
        if category_filter:
            filtered_entries = [e for e in filtered_entries
                                if e.get('category', '').lower() == category_filter.lower()]
            if not filtered_entries:
                print(f"No entries found in category '{category_filter}'")
                return
            
        if sort_by == "title":
            filtered_entries.sort(key=lambda x: x['title'].lower())
        else:  # default to date sorting
            filtered_entries.sort(key=lambda x: x['timestamp'], reverse=True)

        print(f"\nTotal entries: {len(filtered_entries)}")
        for i, entry in enumerate(self.entries, 1):
            print(f"\nEntry #{i}")
            print(f"Title: {entry['title']}")
            print(f"Category: {entry.get('category', 'None')}")
            print(f"Date: {entry['timestamp']}")
            print(f"Content: {entry['content']}")
            print("-" * 40)
        
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
                print(f"Category: {entry.get('category', 'None')}")
                print(f"Date: {entry['timestamp']}")
                print(f"Content: {entry['content']}")
                print("-" * 40)
                found = True
        if not found:
            print(f"No entries found containing '{search_term}'")
        
    def edit_entry(self, index, new_title, new_content, new_category):
        if 0 <= index < len(self.entries):
            entry = self.entries[index]
            if new_title:
                entry['title'] = new_title
            if new_content:
                entry['content'] = new_content
            if new_category:
                entry['category'] = new_category
            entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if save_entries(self.entries):
                print("Entry updated successfully!")
            else:
                print("Failed to update entry - save error.")
        else:
            raise IndexError("Entry index out of range")
        
    def export_entries(self, filename):
        if not filename:
            print("Please provide a filename!")
            return
        try:
            with open(filename, 'w') as f:
                json.dump(self.entries, f, indent=2)
            print(f"Entries exported to {filename}")
        except Exception as e:
            print(f"Export failed: {e}")
        
    def import_entries(self, filename):
        if not filename:
            print("Please provide a filename!")
            return
        try:
            with open(filename, 'r') as f:
                imported_entries = json.load(f)
            self.entries.extend(imported_entries)
            if save_entries(self.entries):
                print(f"Imported {len(imported_entries)} entries from {filename}")
            else:
                print("Failed to save imported entries")
        except Exception as e:
            print(f"Import failed: {e}")