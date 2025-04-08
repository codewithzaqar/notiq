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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()