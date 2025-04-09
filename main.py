import sys
from journal import Journal
from utils import get_user_input, display_menu

def main():
    journal = Journal()
    
    # Handle command-line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--add":
            if len(sys.argv) >= 4:
                journal.add_entry(sys.argv[2], " ".join(sys.argv[3:]))
                return
            else:
                print("Usage: python main.py --add \"title\" \"content\"")
                return
        elif sys.argv[1] == "--view":
            journal.view_entries()
            return
        elif sys.argv[1] == "--help":
            print("Available commands:")
            print("  --add \"title\" \"content\" - Add a new entry")
            print("  --view - View all entries")
            print("  --help - Show this help")
            return
    
    # Interactive mode
    while True:
        display_menu()
        choice = get_user_input("Enter your choice: ")
        
        try:
            if choice == "1":
                title = get_user_input("Enter entry title: ")
                content = get_user_input("Enter entry content: ")
                category = get_user_input("Enter category (optional, press Enter to skip): ")
                journal.add_entry(title, content, category)
            elif choice == "2":
                sort_by = get_user_input("Sort by (date/title, press Enter for default): ").lower()
                journal.view_entries(sort_by or "date")
            elif choice == "3":
                journal.view_entries()
                index = int(get_user_input("Enter entry number to delete: ")) - 1
                journal.delete_entry(index)
            elif choice == "4":
                search_term = get_user_input("Enter search term: ")
                journal.search_entries(search_term)
            elif choice == "5":
                journal.view_entries()
                index = int(get_user_input("Enter entry number to edit: ")) - 1
                new_title = get_user_input("Enter new title (press Enter to keep current): ")
                new_content = get_user_input("Enter new content (press Enter to keep current): ")
                new_category = get_user_input("Enter new category (press Enter to keep current): ")
                journal.edit_entry(index, new_title, new_content, new_category)
            elif choice == "6":
                date_filter = get_user_input("Enter date (YYYY-MM-DD) or press Enter for all: ")
                journal.view_entries(date_filter=date_filter)
            elif choice == "7":
                category_filter = get_user_input("Enter category to filter (press Enter for all): ")
                journal.view_entries(category_filter=category_filter)
            elif choice == "8":
                filename = get_user_input("Enter export filename (e.g., export.json): ")
                journal.export_entries(filename)
            elif choice == "9":
                filename = get_user_input("Enter import filename: ")
                journal.import_entries(filename)
            elif choice == "10":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1-10.")
        except ValueError as e:
            print(f"Input error: {str(e)}")
        except IndexError as e:
            print(f"Index error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()