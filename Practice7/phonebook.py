import csv
from connect import get_connection

# Insert from CSV
def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            name, phone = row
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted!")


# Insert from console
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added!")


# Update contact
def update_contact():
    name = input("Enter existing name: ")
    new_name = input("New name (leave empty to skip): ")
    new_phone = input("New phone (leave empty to skip): ")

    conn = get_connection()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE contacts SET name=%s WHERE name=%s",
            (new_name, name)
        )

    if new_phone:
        cur.execute(
            "UPDATE contacts SET phone=%s WHERE name=%s",
            (new_phone, name)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated!")


# Query contacts
def query_contacts():
    print("\n1. Show all")
    print("2. Search by name")
    print("3. Search by phone prefix")

    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM contacts")

    elif choice == "2":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM contacts WHERE name ILIKE %s",
            (f"%{name}%",)
        )

    elif choice == "3":
        prefix = input("Enter prefix: ")
        cur.execute(
            "SELECT * FROM contacts WHERE phone LIKE %s",
            (f"{prefix}%",)
        )

    rows = cur.fetchall()

    print("\n--- RESULTS ---")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# Delete contact
def delete_contact():
    print("\n1. Delete by name")
    print("2. Delete by phone")

    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted!")


# Main menu
def main():
    while True:
        print("\n📱 PhoneBook Menu")
        print("1. Insert from CSV")
        print("2. Add contact")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
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
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()