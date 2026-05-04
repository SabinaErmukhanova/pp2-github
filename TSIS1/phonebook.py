import psycopg2  # Imports psycopg2, which allows Python to connect to PostgreSQL databases
from connect import get_connection  # Imports our own get_connection function from connect.py
import json  # Imports json module, which is used to read and write JSON files



# Show all contacts with groups and phones
def show_all():  # Defines a function that shows all contacts from the database
    conn = get_connection()  # Opens a connection to the PostgreSQL database
    cur = conn.cursor()  # Creates a cursor object to execute SQL commands
    # get all contacts with group and phone info using JOIN
    cur.execute("""  
        SELECT 
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            p.phone,
            p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.id
    """)  # Selects contact data together with group name and phone information using JOIN

    rows = cur.fetchall()  # Gets all rows returned by the SELECT query

    for row in rows:  # Loops through every returned row
        print(row)  # Prints one contact row

    cur.close()  # Closes the cursor
    conn.close()  # Closes the database connection

# Filter contacts by group
def filter_by_group():  # Defines a function that filters contacts by group
    conn = get_connection()  # Opens a database connection
    cur = conn.cursor()  # Creates a cursor to run SQL queries

    group_name = input("Enter group (Family/Work/Friend/Other): ")  # Asks the user to enter a group name
    # select only contacts from chosen group
    cur.execute("""
        SELECT c.name, c.email, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group_name,))  # Selects only contacts that belong to the entered group

    rows = cur.fetchall()  # Gets all matching contacts

    if not rows:  # Checks if the result is empty
        print("No contacts found")  # Prints message if no contacts were found
    else:  # Runs if contacts were found
        for r in rows:  # Loops through each found contact
            print("Name:", r[0], "| Email:", r[1], "| Group:", r[2])  # Prints contact name, email, and group

    cur.close()  # Closes the cursor
    conn.close()  # Closes the database connection

# Search contacts by name, email or phone
def search():  # Defines a function for searching contacts
    conn = get_connection()  # Opens a database connection
    cur = conn.cursor()  # Creates a cursor object

    query = input("Search (name/email/phone): ")  # Asks the user to enter search text
    # call SQL function search_contacts
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))  # Calls PostgreSQL function search_contacts
    rows = cur.fetchall()  # Gets all search results

    for r in rows:  # Loops through each result
        print(r)  # Prints one result row

    cur.close()  # Closes the cursor
    conn.close()  # Closes the database connection

# Export all contacts to JSON file
def export_json():  # Defines a function that exports contacts to JSON
    conn = get_connection()  # Opens a database connection
    cur = conn.cursor()  # Creates a cursor object
    # select all data needed for JSON
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)  # Selects all data needed for JSON export

    rows = cur.fetchall()  # Gets all selected rows

    data = []  # Creates an empty list that will store dictionaries for JSON

    for r in rows:  # Loops through each database row
        data.append({  # Adds one contact dictionary to the list
            "name": r[0],  # Stores contact name
            "email": r[1],  # Stores contact email
            "birthday": str(r[2]),  # Converts birthday date to string for JSON
            "group": r[3],  # Stores group name
            "phone": r[4],  # Stores phone number
            "type": r[5]  # Stores phone type
        })  # Ends dictionary append
    # write JSON file
    with open("contacts.json", "w") as f:  # Opens contacts.json file in write mode
        json.dump(data, f, indent=4)  # Writes data into JSON file with indentation

    print("Exported!")  # Prints success message

    cur.close()  # Closes the cursor
    conn.close()  # Closes the database connection

# Import contacts from JSON file
def import_json():  # Defines a function that imports contacts from JSON
    conn = get_connection()  # Opens a database connection
    cur = conn.cursor()  # Creates a cursor object
    # read JSON file
    with open("contacts.json", "r") as file:  # Opens contacts.json file in read mode
        data = json.load(file)  # Reads JSON data from the file

    for d in data:  # Loops through each contact dictionary from JSON
        name = d.get("name")  # Gets contact name from JSON
        email = d.get("email")  # Gets email from JSON
        birthday = d.get("birthday")  # Gets birthday from JSON
        group_name = d.get("group")  # Gets group name from JSON
        phone = d.get("phone")  # Gets phone number from JSON
        ptype = d.get("type")  # Gets phone type from JSON
        # get group id
        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))  # Searches group id by group name
        group = cur.fetchone()  # Gets one group row if it exists
        # create group if not exists
        if group:  # Checks if group was found
            group_id = group[0]  # Takes group id from found row
        else:  # Runs if group does not exist
            cur.execute(
                "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                (group_name,)
            )  # Creates new group and returns its id
            group_id = cur.fetchone()[0]  # Stores newly created group id
        # insert contact
        try:  # Tries to insert a new contact
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, group_id))  # Inserts contact and returns contact id

            contact_id = cur.fetchone()[0]  # Saves inserted contact id

        except psycopg2.errors.UniqueViolation:  # Handles duplicate contact name error
            conn.rollback()  # Rolls back failed transaction
            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))  # Finds existing contact id
            contact_id = cur.fetchone()[0]  # Saves existing contact id
        # insert phone
        if phone:  # Checks if phone value exists
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, ptype))  # Inserts phone number connected to contact id

        conn.commit()  # Saves all changes for this contact

    cur.close()  # Closes the cursor
    conn.close()  # Closes the database connection

    print("Imported!")  # Prints success message

# Show contacts page by page
def pagination():  # Defines a function that shows contacts page by page
    conn = get_connection()  # Opens a database connection
    cur = conn.cursor()  # Creates a cursor object

    limit = 3  # Sets number of rows per page
    offset = 0  # Sets starting row position

    while True:  # Starts pagination loop
        # call SQL pagination function
        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )  # Calls PostgreSQL pagination function

        rows = cur.fetchall()  # Gets rows for the current page

        for r in rows:  # Loops through rows on current page
            print(r)  # Prints one row

        cmd = input("next / prev / quit: ")  # Asks user what page action to do

        if cmd == "next":  # Checks if user wants next page
            offset += limit  # Moves offset forward
        elif cmd == "prev":  # Checks if user wants previous page
            offset = max(0, offset - limit)  # Moves offset back but not below zero
        else:  # Runs if user enters quit or something else
            break  # Stops pagination loop

    cur.close()  # Closes the cursor
    conn.close()  # Closes the database connection



# Add new phone to existing contact
def add_phone():  # Defines a function that adds a new phone to an existing contact
    conn = get_connection()  # Opens a database connection
    cur = conn.cursor()  # Creates a cursor object

    name = input("Enter contact name: ")  # Asks user for contact name
    phone = input("Enter phone: ")  # Asks user for new phone number
    ptype = input("Enter type (home/work/mobile): ")  # Asks user for phone type
    # call stored procedure
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))  # Calls PostgreSQL stored procedure add_phone

    conn.commit()  # Saves changes to the database
    cur.close()  # Closes the cursor
    conn.close()  # Closes the database connection

    print("Phone added!")  # Prints success message

# Move contact to another group
def move_to_group():  # Defines a function that moves contact to another group
    conn = get_connection()  # Opens a database connection
    cur = conn.cursor()  # Creates a cursor object

    name = input("Enter contact name: ")  # Asks user for contact name
    group = input("Enter new group: ")  # Asks user for new group name

    cur.execute("CALL move_to_group(%s, %s)", (name, group))  # Calls PostgreSQL stored procedure move_to_group

    conn.commit()  # Saves changes to database
    cur.close()  # Closes the cursor
    conn.close()  # Closes database connection

    print("Moved to group!")  # Prints success message

# Main menu of the program
def main():  # Defines main function with console menu
    while True:  # Starts infinite menu loop
        print("\n1 Show all")  # Prints menu option 1
        print("2 Filter by group")  # Prints menu option 2
        print("3 Search")  # Prints menu option 3
        print("4 Export JSON")  # Prints menu option 4
        print("5 Import JSON")  # Prints menu option 5
        print("6 Pagination")  # Prints menu option 6
        print("7 Exit")  # Prints menu option 7
        print("8 Add phone")  # Prints menu option 8
        print("9 Move to group")  # Prints menu option 9

        c = input("Choose: ")  # Reads user menu choice

        if c == "1":  # Checks if user chose option 1
            show_all()  # Calls show_all function
        elif c == "2":  # Checks if user chose option 2
            filter_by_group()  # Calls filter_by_group function
        elif c == "3":  # Checks if user chose option 3
            search()  # Calls search function
        elif c == "4":  # Checks if user chose option 4
            export_json()  # Calls export_json function
        elif c == "5":  # Checks if user chose option 5
            import_json()  # Calls import_json function
        elif c == "6":  # Checks if user chose option 6
            pagination()  # Calls pagination function
        elif c == "7":  # Checks if user chose option 7
            break  # Stops the program loop
        elif c == "8":  # Checks if user chose option 8
            add_phone()  # Calls add_phone function
        elif c == "9":  # Checks if user chose option 9
            move_to_group()  # Calls move_to_group function


main()  # Starts the program