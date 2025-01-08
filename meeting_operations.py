from database import SQLiteDatabase
from menu import get_input


class MeetingOperations:
    """Class to handle operations related to meetings."""

    def __init__(self, db: SQLiteDatabase):
        self.db = db

    def add_meeting(self) -> None:
        """Add a new meeting to the database."""
        meeting_data = {
            'meeting_name': get_input("Enter meeting name: "),
            'day_of_week': get_input("Enter day of the week: "),
            'time': get_input("Enter time (24-hour format): "),
            'zoom_link': get_input("Enter Zoom link: "),
            'zoom_meeting_id': get_input("Enter Zoom meeting ID: "),
            'zoom_passcode': get_input("Enter Zoom passcode: ")
        }
        self.db.create('Meetings', meeting_data)
        print("Meeting added successfully!")

    def view_meetings(self) -> None:
        """View all meetings in the database."""
        meetings = self.db.read("SELECT * FROM Meetings;")
        if meetings:
            self.db.display(meetings)
        else:
            print("No meetings found.")

    def edit_meeting(self) -> None:
        """Edit an existing meeting."""
        meeting_id = int(get_input("Enter the ID of the meeting to update: "))
        meeting_data = {
            'meeting_name': get_input("Enter new meeting name: "),
            'day_of_week': get_input("Enter new day of the week: "),
            'time': get_input("Enter new time (24-hour format): "),
            'zoom_link': get_input("Enter new Zoom link: "),
            'zoom_meeting_id': get_input("Enter new Zoom meeting ID: "),
            'zoom_passcode': get_input("Enter new Zoom passcode: ")
        }

        for column, new_value in meeting_data.items():
            self.db.update('Meetings', meeting_id, column, new_value)
        print("Meeting updated successfully!")

    def delete_meeting(self) -> None:
        """Delete a meeting by its ID."""
        meeting_id = int(get_input("Enter the ID of the meeting to delete: "))
        self.db.delete('Meetings', meeting_id)
        print("Meeting and associated reminders deleted successfully.")
