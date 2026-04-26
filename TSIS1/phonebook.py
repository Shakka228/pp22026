import json
import csv
from connect import get_connection

conn = get_connection()
cur = conn.cursor()
## -------- ADD CONTACT --------
def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group (Family/Work/Friend/Other): ")

    # insert contact
    cur.execute("""
        INSERT INTO contacts(name, email, birthday)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (name, email, birthday))

    contact_id = cur.fetchone()[0]

    # assign group using procedure
    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    # add phones
    while True:
        phone = input("Phone (empty to stop): ")
        if not phone:
            break

        ptype = input("Type (home/work/mobile): ")

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (contact_id, phone, ptype))

    conn.commit()
    print("✅ Contact added successfully!")


# -------- SEARCH --------
def search():
    query = input("Search: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    for row in cur.fetchall():
        print(row)


# -------- FILTER BY GROUP --------
def filter_by_group():
    group = input("Group: ")
    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))
    for row in cur.fetchall():
        print(row)


# -------- SORT --------
def sort_contacts():
    field = input("Sort by (name/birthday/created_at): ")

    if field not in ["name", "birthday", "created_at"]:
        field = "name"

    cur.execute(f"SELECT name, email FROM contacts ORDER BY {field}")
    for row in cur.fetchall():
        print(row)


# -------- PAGINATION --------
def paginate():
    page = 0
    limit = 3

    while True:
        cur.execute("SELECT * FROM contacts LIMIT %s OFFSET %s", (limit, page*limit))
        rows = cur.fetchall()

        for r in rows:
            print(r)

        cmd = input("next/prev/quit: ")
        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        elif cmd == "quit":
            break


# -------- EXPORT JSON --------
def export_json():
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f, default=str, indent=4)


# -------- IMPORT JSON --------
def import_json():
    with open("contacts.json") as f:
        data = json.load(f)

    for entry in data:
        name = entry[0]

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists (skip/overwrite): ")
            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
        """, (entry[0], entry[1], entry[2]))

    conn.commit()


## -------- DELETE CONTACT --------
def delete_contact():
    name = input("Enter contact name to delete: ")

    cur.execute("SELECT * FROM contacts WHERE name = %s", (name,))
    contact = cur.fetchone()

    if not contact:
        print("❌ Contact not found")
        return

    confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ")

    if confirm.lower() == "yes":
        cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
        conn.commit()
        print("✅ Contact deleted (with all phones)")
    else:
        print("❌ Deletion cancelled")

def delete_phone():
    phone = input("Enter phone to delete: ")

    cur.execute("SELECT * FROM phones WHERE phone = %s", (phone,))
    exists = cur.fetchone()

    if not exists:
        print("❌ Phone not found")
        return

    confirm = input(f"Delete phone {phone}? (yes/no): ")

    if confirm.lower() == "yes":
        cur.execute("DELETE FROM phones WHERE phone = %s", (phone,))
        conn.commit()
        print("✅ Phone deleted")
    else:
        print("❌ Cancelled")

# -------- MENU --------
def menu():
    while True:
        print("""
1 Add contact
2 Search
3 Filter by group
4 Sort
5 Pagination
6 Export JSON
7 Import JSON
8 Delete contact
9 Delete phone
0 Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            search()
        elif choice == "3":
            filter_by_group()
        elif choice == "4":
            sort_contacts()
        elif choice == "5":
            paginate()
        elif choice == "6":
            export_json()
        elif choice == "7":
            import_json()
        elif choice == "8":
            delete_contact()
        elif choice == "9":
            delete_phone()
        elif choice == "0":
            break


menu()