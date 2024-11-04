from database_operations import DatabaseOperations


def create_action_map(db_ops: DatabaseOperations) -> dict:
    return {
        1: db_ops.add_meeting,
        2: db_ops.add_contact,
        3: db_ops.view_meetings,
        4: db_ops.view_contacts,
        5: db_ops.edit_meeting,
        6: db_ops.edit_contact,
        7: db_ops.delete_meeting,
        8: db_ops.delete_contact,
        9: db_ops.assign_participants,
        10: db_ops.remove_participants,
        11: db_ops.view_participants,
        12: db_ops.add_reminder,
        13: db_ops.edit_reminder,
        14: db_ops.delete_reminder,
        15: db_ops.view_reminders,
        16: lambda: print("Exiting...")
    }


def execute_action(action_map: dict):
    while True:
        choice = int(input("Enter your choice: "))  # Simplified for example
        if choice in action_map:
            action_map[choice]()
            if choice == 16:
                break
        else:
            print("Invalid choice, please try again.")

