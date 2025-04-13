# Meeting and Reminder Scheduler

This is a command-line based application for managing meetings, contacts, reminders, and participants, with integrated email notification support via Gmail.

## 📦 Features

- 📅 Add, view, edit, and delete meetings
- 👥 Manage contacts and assign them to meetings
- ⏰ Set up and manage reminders for meetings
- 📧 Send automated reminder emails using Gmail SMTP
- 📋 View and manage participants per meeting
- 🧠 Persistent data stored in SQLite

## 🧱 Requirements

- Python 3.7+
- `apscheduler`
- Environment variables:
  - `TA_REMIND_EMAIL`: Your Gmail address
  - `GMAIL_PASSWORD`: App password for Gmail

## 🚀 Getting Started

1. **Install dependencies:**
   ```bash
   pip install apscheduler
   ```

2. **Set your environment variables:**
   ```bash
   export TA_REMIND_EMAIL='your_email@gmail.com'
   export GMAIL_PASSWORD='your_gmail_app_password'
   ```

3. **Run the main menu:**
   ```bash
   python main.py
   ```

4. **Start the reminder scheduler (in a separate terminal or background process):**
   ```bash
   python scheduler.py
   ```

## 🗃 Database Schema

- **Meetings**: Stores meeting details (name, time, Zoom info)
- **Contacts**: Stores contact information (name, email, phone)
- **Reminders**: Stores reminder timing for meetings
- **Participants**: Many-to-many relationship between contacts and meetings

## ✉️ Email Reminders

Reminders are sent based on day/time entries in the `Reminders` table. Email content adapts based on the meeting location (Zoom, Discord, Office).

## 🛠 Structure

- `main.py`: App entry point and menu dispatcher
- `database.py`: SQLite wrapper for database operations
- `meeting_operations.py`: Meeting management
- `contact_operations.py`: Contact management
- `participant_operations.py`: Participant assignment
- `reminder_operations.py`: Reminder CRUD
- `ta_emails.py`: Email logic
- `scheduler.py`: Background reminder job scheduler

## 🧪 Example Menu

```
1. Add Meeting
2. Add Contact
...
15. View Reminders
16. Exit
```

## 🧼 License

MIT License. Free to use and modify.
