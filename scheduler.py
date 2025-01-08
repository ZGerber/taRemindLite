from apscheduler.schedulers.blocking import BlockingScheduler
from database import SQLiteDatabase
from ta_emails import EmailReminder


class ReminderScheduler:
    """Scheduler for managing reminders."""

    def __init__(self, db_file: str):
        self.db = SQLiteDatabase(db_file)
        self.scheduler = BlockingScheduler()

    def schedule_reminders(self):
        """Fetch reminders from the database and schedule email sending."""
        reminders = self.db.read(
            "SELECT meeting_id, reminder_day, reminder_time FROM Reminders WHERE status = 'Pending'")

        for reminder in reminders:
            meeting_id, reminder_day, reminder_time = reminder
            self.scheduler.add_job(
                func=self.send_email,
                trigger='cron',
                day_of_week=self.abbreviate_weekday(reminder_day),
                hour=self.get_hour(reminder_time),
                minute=self.get_minute(reminder_time),
                args=[meeting_id]
            )

        self.scheduler.add_job(self.reset_reminder_status, 'cron', hour=0, minute=0)

        for job in self.scheduler.get_jobs():
            print(job)
        try:
            print("Starting the reminder scheduler...")
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

    @staticmethod
    def send_email(meeting_id: int):
        """Wrapper function to send email for the given meeting ID."""
        email_reminder = EmailReminder(meeting_id)
        email_reminder.send_email()

    def reset_reminder_status(self):
        """Reset the status of all reminders to 'Pending'."""
        reminders = self.db.read("SELECT id FROM Reminders")
        for reminder in reminders:
            self.db.update('Reminders', reminder[0], 'status', 'Pending')

    @staticmethod
    def abbreviate_weekday(day: str) -> str:
        """Convert full weekday name to its abbreviation for cron."""
        weekdays = {
            'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed',
            'Thursday': 'Thu', 'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'
        }
        return weekdays.get(day, '')

    @staticmethod
    def get_hour(reminder_time: str) -> int:
        """Extract the hour from the reminder time."""
        return int(reminder_time.split(':')[0])

    @staticmethod
    def get_minute(reminder_time: str) -> int:
        """Extract the minute from the reminder time."""
        return int(reminder_time.split(':')[1])


def main():
    scheduler = ReminderScheduler("meetings.db")
    scheduler.schedule_reminders()


if __name__ == "__main__":
    main()
