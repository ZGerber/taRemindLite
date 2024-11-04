import sqlite3
from database import SQLiteDatabase, connect_to_db
from menu import get_input


class DatabaseOperations:
    def __init__(self, db: SQLiteDatabase):
        self.db = db

    def add_meeting(self) -> None:
        meeting_data = {
            'meeting_name': get_input("Enter meeting name: "),
            'day_of_week': get_input("Enter day of the week: "),
            'time': get_input("Enter time (24-hour format): "),
            'zoom_link': get_input("Enter Zoom link: "),
            'zoom_meeting_id': get_input("Enter Zoom meeting ID: "),
            'zoom_passcode': get_input("Enter Zoom passcode: ")
        }
        self.db.add('Meetings', meeting_data)
        print("Meeting added successfully!")

    def add_contact(self) -> None:
        contact_data = {
            'first_name': get_input("Enter first name: "),
            'last_name': get_input("Enter last name: "),
            'email': get_input("Enter email: "),
            'phone_number': get_input("Enter phone number: ")
        }
        self.db.add('Contacts', contact_data)
        print("Contact added successfully!")

    def view_meetings(self) -> None:
        meetings = self.db.query("SELECT * FROM Meetings;")
        if meetings:
            self.db.display(meetings)
        else:
            print("No meetings found.")

    def view_contacts(self) -> None:
        contacts = self.db.query("SELECT * FROM Contacts;")
        if contacts:
            self.db.display(contacts)
        else:
            print("No contacts found.")

    def edit_meeting(self) -> None:
        meeting_id = int(get_input("Enter the ID of the meeting to edit: "))
        meeting_data = {
            'meeting_name': get_input("Enter new meeting name: "),
            'day_of_week': get_input("Enter new day of the week: "),
            'time': get_input("Enter new time (24-hour format): "),
            'zoom_link': get_input("Enter new Zoom link: "),
            'zoom_meeting_id': get_input("Enter new Zoom meeting ID: "),
            'zoom_passcode': get_input("Enter new Zoom passcode: ")
        }

        for column, new_value in meeting_data.items():
            self.db.edit('Meetings', meeting_id, column, new_value)
        print("Meeting updated successfully!")

    def edit_contact(self) -> None:
        contact_id = int(get_input("Enter the ID of the contact to edit: "))
        contact_data = {
            'first_name': get_input("Enter new first name: "),
            'last_name': get_input("Enter new last name: "),
            'email': get_input("Enter new email: "),
            'phone_number': get_input("Enter new phone number: ")
        }

        for column, new_value in contact_data.items():
            self.db.edit('Contacts', contact_id, column, new_value)
        print("Contact updated successfully!")

    def delete_meeting(self) -> None:
        meeting_id = int(get_input("Enter the ID of the meeting to delete: "))
        self.db.delete('Meetings', meeting_id)
        print("Meeting and associated reminders deleted successfully.")

    def delete_contact(self) -> None:
        contact_id = int(get_input("Enter the ID of the contact to delete: "))
        self.db.delete('Contacts', contact_id)
        print("Contact deleted successfully.")

    def assign_participants(self) -> None:
        meeting_id = int(get_input("Enter the meeting ID to assign participants to: "))
        participant_ids = list(map(int, get_input("Enter participant IDs separated by commas: ").split(',')))
        try:
            with connect_to_db(self.db.db_file) as cursor:
                for contact_id in participant_ids:
                    cursor.execute('''
                    INSERT INTO Participants (meeting_id, contact_id)
                    VALUES (?, ?)''', (meeting_id, contact_id))
            print("Participants assigned successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred while assigning participants: {e}")

    def remove_participants(self) -> None:
        meeting_id = int(get_input("Enter the meeting ID to remove participants from: "))
        participant_ids = list(map(int, get_input("Enter participant IDs separated by commas: ").split(',')))
        try:
            with connect_to_db(self.db.db_file) as cursor:
                for contact_id in participant_ids:
                    cursor.execute('''
                    DELETE FROM Participants
                    WHERE meeting_id = ? AND contact_id = ?''', (meeting_id, contact_id))
            print("Participants removed successfully!")
        except sqlite3.Error as e:
            print(f"An error occurred while unassigning participants: {e}")

    def view_participants(self) -> None:
        meeting_id = int(get_input("Enter the meeting ID to view participants for: "))
        participants = self.db.query('''
        SELECT Contacts.id, Contacts.first_name, Contacts.last_name, Contacts.email
        FROM Participants
        JOIN Contacts ON Participants.contact_id = Contacts.id
        WHERE Participants.meeting_id = ?;''', (meeting_id,))

        if participants:
            self.db.display(participants)
        else:
            print(f"No participants found for Meeting ID {meeting_id}.")

    def add_reminder(self) -> None:
        meeting_id = int(get_input("Enter the meeting ID to add a reminder for: "))
        reminder_data = {
            'meeting_id': meeting_id,
            'reminder_day': get_input("Enter reminder day (e.g., 'Monday'): "),
            'reminder_time': get_input("Enter reminder time (24-hour format): "),
            'status': 'Pending'  # Default status
        }
        self.db.add('Reminders', reminder_data)
        print("Reminder added successfully!")

    def edit_reminder(self) -> None:
        reminder_id = int(get_input("Enter the ID of the reminder to edit: "))
        reminder_day = get_input("Enter new reminder day: ")
        reminder_time = get_input("Enter new reminder time (24-hour format): ")
        self.db.edit('Reminders', reminder_id, 'reminder_day', reminder_day)
        self.db.edit('Reminders', reminder_id, 'reminder_time', reminder_time)
        print("Reminder updated successfully!")

    def delete_reminder(self) -> None:
        reminder_id = int(get_input("Enter the ID of the reminder to delete: "))
        self.db.delete('Reminders', reminder_id)
        print("Reminder deleted successfully!")

    def view_reminders(self) -> None:
        reminders = self.db.query("SELECT * FROM Reminders;")
        if reminders:
            self.db.display(reminders)
        else:
            print("No reminders found.")
