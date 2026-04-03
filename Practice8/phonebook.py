# Import required libraries
import psycopg2
from connect import get_connection
import csv


# Function to create table in database
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# Function to insert data from CSV file
def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", "r") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) != 2:
                continue  # skip incorrect rows

            name, phone = row

            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()


# Function to insert data manually
def insert_from_console():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


# Function to update contact (old way)
def update_contact():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Enter name to update: ")
    new_phone = input("Enter new phone: ")

    cur.execute(
        "UPDATE contacts SET phone = %s WHERE name = %s",
        (new_phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()


# Search using PostgreSQL FUNCTION
def query_contacts():
    conn = get_connection()
    cur = conn.cursor()

    pattern = input("Enter search (name or phone): ")

    # Call SQL function
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))

    rows = cur.fetchall()

    if not rows:
        print("No contacts found")

    for row in rows:
        print("ID:", row[0], "| Name:", row[1], "| Phone:", row[2])

    cur.close()
    conn.close()


#  Pagination using SQL FUNCTION
def paginate_contacts():
    conn = get_connection()
    cur = conn.cursor()

    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit, offset)
    )

    rows = cur.fetchall()

    for row in rows:
        print("ID:", row[0], "| Name:", row[1], "| Phone:", row[2])

    cur.close()
    conn.close()


#  Insert or Update using PROCEDURE
def insert_or_update_proc():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))

    conn.commit()
    conn.close()

    print("Inserted or updated!")


#  Bulk insert using PROCEDURE
def insert_many():
    conn = get_connection()
    cur = conn.cursor()

    names = input("Enter names (comma separated): ").split(',')
    phones = input("Enter phones (comma separated): ").split(',')

    cur.execute(
        "CALL insert_many_users(%s, %s)",
        (names, phones)
    )

    conn.commit()
    conn.close()

    print("Bulk insert done!")


#  Delete using PROCEDURE
def delete_user_proc():
    conn = get_connection()
    cur = conn.cursor()

    value = input("Enter name or phone to delete: ")

    cur.execute("CALL delete_user(%s)", (value,))

    conn.commit()
    conn.close()

    print("Deleted!")


# OLD delete
def delete_contact():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Enter name to delete: ")

    cur.execute(
        "DELETE FROM contacts WHERE name = %s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()

# Function to show ALL contacts (table view)
def show_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    # Get all data from table
    cur.execute("SELECT * FROM contacts ORDER BY id")

    rows = cur.fetchall()

    print("\n=== CONTACTS TABLE ===")
    print("ID | Name       | Phone")
    print("----------------------------")

    # Print nicely
    for row in rows:
        print(f"{row[0]}  | {row[1]:10} | {row[2]}")

    cur.close()
    conn.close()


# Main program
def main():
    create_table()

    while True:
        print("\n1. Insert CSV")
        print("2. Insert console")
        print("3. Update (old)")
        print("4. Search (function)")
        print("5. Delete (old)")
        print("6. Exit")
        print("7. Pagination")
        print("8. Insert/Update (procedure)")
        print("9. Bulk insert")
        print("10. Delete (procedure)")
        print("11. Show all contacts")

        choice = input("Choose: ")

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
            break
        elif choice == "7":
            paginate_contacts()
        elif choice == "8":
            insert_or_update_proc()
        elif choice == "9":
            insert_many()
        elif choice == "10":
            delete_user_proc()
        elif choice == "11":
            show_all_contacts()


# Run program
main()