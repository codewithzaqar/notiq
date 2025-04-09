from datetime import datetime
import re
import json
from base64 import b64encode, b64decode
from storage import save_entries, load_entries

class Journal:
    ENCRYPTION_KEY = "jrnl_simple_key"  # Simple key for basic obfuscation

    def __init__(self):
        self.entries = load_entries() or []

    def _encrypt(self, text):
        return b64encode(text.encode('utf-8')).decode('utf-8')

    def _decrypt(self, encrypted_text):
        try:
            return b64decode(encrypted_text.encode('utf-8')).decode('utf-8')
        except UnicodeDecodeError as e:
            raise ValueError(f"Decoding error: {str(e)}. Data may be corrupted or from an incompatible version.")
        except Exception as e:
            raise ValueError(f"Decryption error: {str(e)}. Invalid Base64 data.")

    def add_entry(self, title, content, category=""):
        if not title or not content:
            raise ValueError("Title and content cannot be empty")
        entry = {
            "title": self._encrypt(title),
            "content": self._encrypt(content),
            "category": self._encrypt(category) if category else "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.entries.append(entry)
        if not save_entries(self.entries):
            raise IOError("Failed to save entry to storage")

    def view_entries(self, sort_by="date", date_filter="", category_filter=""):
        if not self.entries:
            print("No entries found.")
            return
        
        filtered_entries = self.entries.copy()
        if date_filter:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_filter):
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
            filtered_entries = [e for e in filtered_entries 
                              if e['timestamp'].startswith(date_filter)]
            if not filtered_entries:
                print(f"No entries found for {date_filter}")
                return

        if category_filter:
            encrypted_filter = self._encrypt(category_filter)
            filtered_entries = [e for e in filtered_entries 
                              if e.get('category', '') == encrypted_filter]
            if not filtered_entries:
                print(f"No entries found in category '{category_filter}'")
                return

        if sort_by == "title":
            filtered_entries.sort(key=lambda x: self._decrypt(x['title']).lower())
        else:  # default to date sorting
            filtered_entries.sort(key=lambda x: x['timestamp'], reverse=True)

        print(f"\nTotal entries: {len(filtered_entries)}")
        for i, entry in enumerate(filtered_entries, 1):
            try:
                print(f"\nEntry #{i}")
                print(f"Title: {self._decrypt(entry['title'])}")
                print(f"Category: {self._decrypt(entry['category']) if entry['category'] else 'None'}")
                print(f"Date: {entry['timestamp']}")
                print(f"Content: {self._decrypt(entry['content'])}")
                print("-" * 40)
            except ValueError as e:
                print(f"\nEntry #{i} - Error: {str(e)}")
                print("-" * 40)

    def delete_entry(self, index):
        if not 0 <= index < len(self.entries):
            raise IndexError("Entry number out of range")
        deleted_entry = self.entries.pop(index)
        if not save_entries(self.entries):
            raise IOError(f"Failed to delete entry: {self._decrypt(deleted_entry['title'])}")

    def search_entries(self, search_term):
        found = False
        print(f"\nSearch results for '{search_term}':")
        for i, entry in enumerate(self.entries, 1):
            try:
                if search_term.lower() in self._decrypt(entry['title']).lower():
                    print(f"\nEntry #{i}")
                    print(f"Title: {self._decrypt(entry['title'])}")
                    print(f"Category: {self._decrypt(entry['category']) if entry['category'] else 'None'}")
                    print(f"Date: {entry['timestamp']}")
                    print(f"Content: {self._decrypt(entry['content'])}")
                    print("-" * 40)
                    found = True
            except ValueError as e:
                print(f"\nEntry #{i} - Error: {str(e)}")
        if not found and not any(isinstance(e, ValueError) for e in self.entries):
            print("No matching entries found.")

    def edit_entry(self, index, new_title, new_content, new_category):
        if not 0 <= index < len(self.entries):
            raise IndexError("Entry number out of range")
        entry = self.entries[index]
        if new_title:
            entry['title'] = self._encrypt(new_title)
        if new_content:
            entry['content'] = self._encrypt(new_content)
        if new_category:
            entry['category'] = self._encrypt(new_category)
        entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not save_entries(self.entries):
            raise IOError("Failed to save updated entry")

    def export_entries(self, filename):
        if not filename:
            raise ValueError("Filename cannot be empty")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, indent=2)
            print(f"Entries exported to {filename}")
        except Exception as e:
            raise IOError(f"Export failed: {str(e)}")

    def import_entries(self, filename):
        if not filename:
            raise ValueError("Filename cannot be empty")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_entries = json.load(f)
            # Validate imported entries
            for entry in imported_entries:
                if not all(key in entry for key in ['title', 'content', 'timestamp']):
                    raise ValueError("Invalid entry format in import file")
            self.entries.extend(imported_entries)
            if not save_entries(self.entries):
                raise IOError("Failed to save imported entries")
            print(f"Imported {len(imported_entries)} entries from {filename}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {str(e)}")
        except Exception as e:
            raise IOError(f"Import failed: {str(e)}")