def display_menu():
    print("\n=== Notiq v0.02 ===")
    print("1. Add new entry")
    print("2. View all entries")
    print("3. Delete entry")
    print("4. Search entries")
    print("5. Exit")
    print("==================")

def get_user_input(prompt):
    return input(prompt).strip()