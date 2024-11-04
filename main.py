from database import SQLiteDatabase
from meeting_operations import MeetingOperations
from contact_operations import ContactOperations
from reminder_operations import ReminderOperations
from participant_operations import ParticipantOperations
from menu import display_menu, get_input


def main():
    """Main function to run the application."""
    db_file = "meetings.db"
    db = SQLiteDatabase(db_file)

    # Instantiate operation classes
    meeting_ops = MeetingOperations(db)
    contact_ops = ContactOperations(db)
    reminder_ops = ReminderOperations(db)
    participant_ops = ParticipantOperations(db)

    # Mapping of user choices to operations
    actions = {
        1: meeting_ops.add_meeting,
        2: contact_ops.add_contact,
        3: meeting_ops.view_meetings,
        4: contact_ops.view_contacts,
        5: meeting_ops.edit_meeting,
        6: contact_ops.edit_contact,
        7: meeting_ops.delete_meeting,
        8: contact_ops.delete_contact,
        9: participant_ops.assign_participants,
        10: participant_ops.remove_participants,
        11: participant_ops.view_participants,
        12: reminder_ops.add_reminder,
        13: reminder_ops.edit_reminder,
        14: reminder_ops.delete_reminder,
        15: reminder_ops.view_reminders,
        16: lambda: print("Exiting..."),
    }

    while True:
        display_menu()
        choice = int(get_input("Enter your choice: "))

        if choice in actions:
            if choice == 16:
                actions[choice]()
                break
            else:
                actions[choice]()
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
