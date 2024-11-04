from apscheduler.schedulers.blocking import BlockingScheduler
from database import SQLiteDatabase
from ta_emails import EmailReminder

# Database instance
db = SQLiteDatabase("/home/zane/software/taRemindLite/meetings.db")


def schedule_reminders():
    """Fetch reminders from the database and schedule email sending."""
    scheduler = BlockingScheduler()

    reminders = db.query("SELECT meeting_id, reminder_day, reminder_time FROM Reminders WHERE status = 'Pending'")

    for reminder in reminders:
        meeting_id = reminder[0]
        reminder_day = reminder[1]
        reminder_time = reminder[2]

        # Schedule the email sending using a cron trigger
        scheduler.add_job(
            func=send_email,
            trigger='cron',
            day_of_week=abbreviate_weekday(reminder_day),
            hour=get_hour(reminder_time),
            minute=get_minute(reminder_time),
            args=[meeting_id]
        )

    scheduler.add_job(reset_reminder_status, 'cron', hour=0, minute=0)

    try:
        print("Starting the reminder scheduler...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def send_email(meeting_id):
    """Wrapper function to send email for the given meeting ID."""
    email_reminder = EmailReminder(meeting_id)
    email_reminder.send_email()


def reset_reminder_status():
    """Reset the status of all reminders to 'Pending'."""
    reminders = db.query("SELECT id FROM Reminders")
    for reminder in reminders:
        db.edit('Reminders', reminder[0], 'status', 'Pending')


def abbreviate_weekday(day: str) -> str:
    """Convert full weekday name to its abbreviation for cron (e.g., 'Monday' to 'mon')."""
    return {
        'Monday': 'Mon',
        'Tuesday': 'Tue',
        'Wednesday': 'Wed',
        'Thursday': 'Thu',
        'Friday': 'Fri',
        'Saturday': 'Sat',
        'Sunday': 'Sun'
    }.get(day, '')


def get_hour(reminder_time: str) -> int:
    """Extract the hour from the reminder time."""
    return int(reminder_time.split(':')[0])


def get_minute(reminder_time: str) -> int:
    """Extract the minute from the reminder time."""
    return int(reminder_time.split(':')[1])


def main():
    schedule_reminders()


if __name__ == "__main__":
    main()
