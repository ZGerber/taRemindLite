
def display_menu() -> None:
    print("\nMenu:")
    print("1. Add Meeting")
    print("2. Add Contact")
    print("3. View Meetings")
    print("4. View Contacts")
    print("5. Edit Meeting")
    print("6. Edit Contact")
    print("7. Delete Meeting")
    print("8. Delete Contact")
    print("9. Assign Participants")
    print("10. Remove Participants")
    print("11. View Participants")
    print("12. Add Reminder")
    print("13. Edit Reminder")
    print("14. Delete Reminder")
    print("15. View Reminders")
    print("16. Exit")


def get_input(prompt: str) -> str:
    return input(prompt).strip()

