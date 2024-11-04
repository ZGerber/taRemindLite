from database import SQLiteDatabase
from menu import get_input


class ParticipantOperations:
    """Class to handle operations related to meeting participants."""

    def __init__(self, db: SQLiteDatabase):
        self.db = db

    def assign_participants(self) -> None:
        """Assign participants to a meeting."""
        meeting_id = int(get_input("Enter the meeting ID to assign participants to: "))
        participant_ids = list(map(int, get_input("Enter participant IDs separated by commas: ").split(',')))

        for participant_id in participant_ids:
            self.db.create('Participants', {'meeting_id': meeting_id, 'contact_id': participant_id})
        print("Participants assigned successfully!")

    def remove_participants(self) -> None:
        """Remove participants from a meeting."""
        meeting_id = int(get_input("Enter the meeting ID to remove participants from: "))
        participant_ids = list(map(int, get_input("Enter participant IDs separated by commas: ").split(',')))

        for participant_id in participant_ids:
            self.db.delete('Participants', (meeting_id, participant_id))
        print("Participants removed successfully!")

    def view_participants(self) -> None:
        """View all participants of a meeting."""
        meeting_id = int(get_input("Enter the meeting ID to view participants: "))
        participants = self.db.read('''
        SELECT Contacts.*
        FROM Participants
        JOIN Contacts ON Participants.contact_id = Contacts.id
        WHERE Participants.meeting_id = ?;
        ''', (meeting_id,))
        if participants:
            self.db.display(participants)
        else:
            print("No participants found for this meeting.")
