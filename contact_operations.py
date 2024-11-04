from database import SQLiteDatabase
from menu import get_input


class ContactOperations:
    """Class to handle operations related to contacts."""

    def __init__(self, db: SQLiteDatabase):
        self.db = db

    def add_contact(self) -> None:
        """Add a new contact to the database."""
        contact_data = {
            'first_name': get_input("Enter first name: "),
            'last_name': get_input("Enter last name: "),
            'email': get_input("Enter email: "),
            'phone_number': get_input("Enter phone number: ")
        }
        self.db.create('Contacts', contact_data)
        print("Contact added successfully!")

    def view_contacts(self) -> None:
        """View all contacts in the database."""
        contacts = self.db.read("SELECT * FROM Contacts;")
        if contacts:
            self.db.display(contacts)
        else:
            print("No contacts found.")

    def edit_contact(self) -> None:
        """Edit an existing contact."""
        contact_id = int(get_input("Enter the ID of the contact to update: "))
        contact_data = {
            'first_name': get_input("Enter new first name: "),
            'last_name': get_input("Enter new last name: "),
            'email': get_input("Enter new email: "),
            'phone_number': get_input("Enter new phone number: ")
        }

        for column, new_value in contact_data.items():
            self.db.update('Contacts', contact_id, column, new_value)
        print("Contact updated successfully!")

    def delete_contact(self) -> None:
        """Delete a contact by its ID."""
        contact_id = int(get_input("Enter the ID of the contact to delete: "))
        self.db.delete('Contacts', contact_id)
        print("Contact deleted successfully.")
