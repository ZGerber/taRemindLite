from database import SQLiteDatabase
from menu import get_input


class ReminderOperations:
    """Class to handle operations related to reminders."""

    def __init__(self, db: SQLiteDatabase):
        self.db = db

    def add_reminder(self) -> None:
        """Add a new reminder for a meeting."""
        meeting_id = int(get_input("Enter the meeting ID for the reminder: "))
        reminder_data = {
            'meeting_id': meeting_id,
            'reminder_day': get_input("Enter reminder day: "),
            'reminder_time': get_input("Enter reminder time: ")
        }
        self.db.create('Reminders', reminder_data)
        print("Reminder added successfully!")

    def edit_reminder(self) -> None:
        """Edit an existing reminder."""
        reminder_id = int(get_input("Enter the ID of the reminder to update: "))
        reminder_data = {
            'reminder_day': get_input("Enter new reminder day: "),
            'reminder_time': get_input("Enter new reminder time: ")
        }

        for column, new_value in reminder_data.items():
            self.db.update('Reminders', reminder_id, column, new_value)
        print("Reminder updated successfully!")

    def delete_reminder(self) -> None:
        """Delete a reminder by its ID."""
        reminder_id = int(get_input("Enter the ID of the reminder to delete: "))
        self.db.delete('Reminders', reminder_id)
        print("Reminder deleted successfully.")

    def view_reminders(self) -> None:
        """View all reminders in the database."""
        reminders = self.db.read("SELECT * FROM Reminders;")
        if reminders:
            self.db.display(reminders)
        else:
            print("No reminders found.")
