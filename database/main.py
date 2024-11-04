from database import SQLiteDatabase
from database_operations import DatabaseOperations
from actions import create_action_map, execute_action
import menu


def main():
    db_file = "/home/zane/software/taRemindLite/meetings.db"
    db = SQLiteDatabase(db_file)
    db_ops = DatabaseOperations(db)
    action_map = create_action_map(db_ops)

    menu.display_menu()
    execute_action(action_map)


if __name__ == "__main__":
    main()
