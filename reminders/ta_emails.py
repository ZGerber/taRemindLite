import smtplib
import ssl
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import List
from database import SQLiteDatabase
import os

# Configuration constants
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

# Environment variables
SENDER: str = os.environ.get("TA_REMIND_EMAIL")
PASSWORD: str = os.environ.get("GMAIL_PASSWORD")

# Database instance
db = SQLiteDatabase("/home/zane/software/taRemindLite/meetings.db")


class EmailReminder:
    def __init__(self, meeting_id: int):
        self.meeting_id = meeting_id

    def get_meeting_details(self) -> dict:
        """Fetch meeting details as a dictionary."""
        return {
            "name": db.get_property("Meetings", self.meeting_id, "meeting_name"),
            "day": db.get_property("Meetings", self.meeting_id, "day_of_week"),
            "time": db.get_property("Meetings", self.meeting_id, "time"),
            "zoom_link": db.get_property("Meetings", self.meeting_id, "zoom_link"),
            "zoom_id": db.get_property("Meetings", self.meeting_id, "zoom_meeting_id"),
            "passcode": db.get_property("Meetings", self.meeting_id, "zoom_passcode"),
        }

    @staticmethod
    def get_day_of_week(meeting_day: str) -> str:
        """Determine the weekday description for the email body."""
        if meeting_day == datetime.now().strftime('%A'):
            return "today"
        elif meeting_day == (datetime.now() + timedelta(1)).strftime('%A'):
            return "tomorrow"
        else:
            return meeting_day

    def recipients(self) -> List[str]:
        """Fetch email addresses of participants."""
        sql = '''
        SELECT Contacts.email
        FROM Participants
        JOIN Contacts ON Participants.contact_id = Contacts.id
        WHERE Participants.meeting_id = ?;'''
        results = db.query(sql, (self.meeting_id,))
        return [row[0] for row in results]

    def email_subject(self) -> str:
        """Construct email subject."""
        return f'Reminder: {self.get_meeting_details()["name"]}'

    def email_body(self) -> str:
        """Construct email body."""
        details = self.get_meeting_details()
        return f"""
        Hi everyone,

        This is a reminder that the {details['name']} is {self.get_day_of_week(details['day'])} at {details['time']} MST over Zoom.

        {details['zoom_link']}

        Meeting ID: {details['zoom_id']}
        Passcode: {details['passcode']}
        """

    def create_email(self) -> str:
        """Create the email message."""
        email = EmailMessage()
        email['From'] = SENDER
        email['To'] = ", ".join(self.recipients())
        email['Subject'] = self.email_subject()
        email.set_content(self.email_body())
        return email.as_string()

    def send_email(self) -> None:
        """Send the email."""
        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=ssl.create_default_context()) as smtp:
                smtp.login(SENDER, PASSWORD)
                smtp.sendmail(SENDER, self.recipients(), self.create_email())
            print(f"{self.get_meeting_details()['name']} email sent: {datetime.now()}")
        except Exception as e:
            print(f"Failed to send email: {e}")
