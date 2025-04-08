from journal import Journal
from utils import get_user_input, display_menu

def main():
    journal = Journal()

    while True:
        display_menu()
        choice = get_user_input("Enter your choice: ")

        if choice == "1":
            title = get_user_input("Enter entry title: ")
            content = get_user_input("Enter entry content: ")
            journal.add_entry(title, content)
        elif choice == "2":
            journal.view_entries()
        elif choice == "3":
            journal.view_entries()
            try:
                index = int(get_user_input("Enter entry number to delete: ")) - 1
                journal.delete_entry(index)
            except ValueError:
                print("Please enter a valid number.")
            except IndexError:
                print("Invalid entry number.")
        elif choice == "4":
            search_term = get_user_input("Enter search term: ")
            journal.search_entries(search_term)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()