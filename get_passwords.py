import sqlite3
from termcolor import colored

def find_all():
    cur.execute("SELECT * FROM Passwords")

    all_rows = cur.fetchall()

    # rows in an array of tuples of shape (website, email, username, password)

    for index, row in enumerate(all_rows):
        print(colored(f"\nENTRY {index + 1}", 'green'))

        print(f"""
          website  : {row[0]}
          email    : {row[1]}
          username : {row[2]}
          password : {row[3]}
        """)


def find_record(site):
    cur.execute("SELECT * FROM Passwords WHERE website = ? ", (site,))

    row = cur.fetchone()

    # row is a tuple

    print(f"""
      website  : {row[0]}
      email    : {row[1]}
      username : {row[2]}
      password : {row[3]}
    """)



def retrieve_saved_passwords():
    global connection, cur

    connection = sqlite3.connect('database.sqlite3')
    cur = connection.cursor()

    find_website = input("Enter the website (press enter to view all records): ")

    if len(find_website) < 1:
        find_all()

    else:
        find_record(find_website)

    cur.close()