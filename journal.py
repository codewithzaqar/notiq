from datetime import datetime
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

    def view_entries(self, sort_by="date", date_filter=""):
        if not self.entries:
            print("No entries found.")
            return
        
        filtered_entries = self.entries
        if date_filter:
            try:
                filtered_entries = [e for e in self.entries 
                                    if e['timestamp'].startswith(date_filter)]
                if not filtered_entries:
                    print(f"No entries found for {date_filter}")
                    return
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD")
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