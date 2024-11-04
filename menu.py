def display_menu() -> None:
    """Display the main menu options."""
    print("\nMenu:")
    options = [
        "1. Add Meeting",
        "2. Add Contact",
        "3. View Meetings",
        "4. View Contacts",
        "5. Edit Meeting",
        "6. Edit Contact",
        "7. Delete Meeting",
        "8. Delete Contact",
        "9. Assign Participants",
        "10. Remove Participants",
        "11. View Participants",
        "12. Add Reminder",
        "13. Edit Reminder",
        "14. Delete Reminder",
        "15. View Reminders",
        "16. Exit"
    ]
    print("\n".join(options))


def get_input(prompt: str) -> str:
    """Get user input with a given prompt."""
    return input(prompt)
