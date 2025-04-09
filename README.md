# Notiq

Notiq is a lightweight, command-line based journal application written in Python. It allows users to create, view, delete, and search journal entries with persistent storage.

## Installation
1. Ensure you have Python 3.x installed
2. Clone or download this repository
3. Navigate to the project directory
4. Run the application

```
python main.py
```

## Usage
Run the program and use the menu options:
1. Add new entry - Create a new journal entry
2. View all entries - Display all entries with sort option (date/title)
3. Delete entry - Remove an entry by its number
4. Search entries - Find entries by title keyword
5. Edit entry - Modify an existing entry
6. Filter by date - Show entries for a specific date
7. Filter by category - Show entries in a specific category
8. Export entries - Save all entries to a JSON file
9. Import entries - Load entries from a JSON file
10. Exit - Close the application

Entries are automatically saved to `journal_entries.json` in the same directory.