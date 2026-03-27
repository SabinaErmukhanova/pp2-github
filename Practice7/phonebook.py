# Import required libraries
import psycopg2              # PostgreSQL connection
from connect import get_connection  # our custom connection function
import csv                  # used to read CSV file


# Function to create table in database
def create_table():
    # Get connection to database
    conn = get_connection()

    # Create cursor → object that executes SQL commands
    cur = conn.cursor()

    # SQL query:
    # CREATE TABLE IF NOT EXISTS → prevents error if table already exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,   
            name VARCHAR(100),       
            phone VARCHAR(20)        
        )
    """)

    # commit() → saves changes in database
    conn.commit()

    # Close cursor → free resources
    cur.close()

    # Close connection
    conn.close()


# Function to insert data from CSV file
def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    # Open file in read mode
    # with → automatically closes file after block ends
    with open("contacts.csv", "r") as file:

        # csv.reader → reads file line by line
        reader = csv.reader(file)

        # Loop through each row in CSV
        for row in reader:
            # Each row contains 2 values: name, phone
            name, phone = row

            # Execute SQL INSERT query
            # %s → placeholder for safe insertion (prevents SQL injection)
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (name, phone)   # values passed as tuple
            )

    conn.commit()
    cur.close()
    conn.close()


# Function to insert data manually from user input
def insert_from_console():
    conn = get_connection()
    cur = conn.cursor()

    # input() → read data from user
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    # Insert into table
    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


# Function to update existing contact
def update_contact():
    conn = get_connection()
    cur = conn.cursor()

    # Ask user which contact to update
    name = input("Enter name to update: ")

    # Ask for new phone number
    new_phone = input("Enter new phone: ")

    # SQL UPDATE query
    # Updates phone WHERE name matches
    cur.execute(
        "UPDATE contacts SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()


# Function to search contacts with filter
def query_contacts():
    conn = get_connection()
    cur = conn.cursor()

    # Ask user for phone prefix (example: 123)
    prefix = input("Enter phone prefix: ")

    # SQL SELECT with LIKE
    # prefix + "%" → finds numbers starting with prefix
    cur.execute(
        "SELECT * FROM contacts WHERE phone LIKE %s",
        (prefix + "%",)
    )

    # fetchall() → gets all results from query
    rows = cur.fetchall()

    # Loop through results
    for row in rows:
        # row → tuple (id, name, phone)
        print(row)

    cur.close()
    conn.close()


# Function to delete contact
def delete_contact():
    conn = get_connection()
    cur = conn.cursor()

    # Ask user which contact to delete
    name = input("Enter name to delete: ")

    # SQL DELETE query
    cur.execute(
        "DELETE FROM contacts WHERE name = %s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()


# Main program (menu system)
def main():
    # Ensure table exists before using it
    create_table()

    # Infinite loop → program runs until user exits
    while True:
        print("\n1. Insert CSV")
        print("2. Insert console")
        print("3. Update")
        print("4. Query")
        print("5. Delete")
        print("6. Exit")

        # Get user choice
        choice = input("Choose: ")

        # Call corresponding function
        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            # Break loop → exit program
            break


# Run main function (entry point)
main()