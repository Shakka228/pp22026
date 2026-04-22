from connect import connect


def search():
    pattern = input("Enter search pattern: ")
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def paginate():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def upsert():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


def bulk_insert():
    names = ["Alice", "Bob", "Charlie"]
    phones = ["12345", "abc", "67890"]

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL bulk_insert_contacts(%s, %s)", (names, phones))

    conn.commit()
    cur.close()
    conn.close()


def delete():
    value = input("Enter name or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()


def menu():
    while True:
        print("\n1. Search")
        print("2. Pagination")
        print("3. Upsert")
        print("4. Bulk Insert")
        print("5. Delete")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            search()
        elif choice == "2":
            paginate()
        elif choice == "3":
            upsert()
        elif choice == "4":
            bulk_insert()
        elif choice == "5":
            delete()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


menu()