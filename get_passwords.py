import sqlite3
from termcolor import colored

def find_all():
    try:
        cur.execute("SELECT * FROM Passwords")

    except:
        print(colored("There are no records to show", 'green'))

    all_rows = cur.fetchall()

    # rows in an array of tuples of shape (website, email, username, password)

    for index, row in enumerate(all_rows):
        print(colored(f"\nENTRY {index + 1}", 'green'))

        print(f"""
          website  : {row[1]}
          email    : {row[2]}
          username : {row[3]}
          password : {row[4]}
        """)


def find_record(site):
    cur.execute("SELECT * FROM Passwords WHERE website = ? ", (site,))

    row = cur.fetchone()

    # row is a tuple
    if row is not None:
        print(f"""
        website  : {row[1]}
        email    : {row[2]}
        username : {row[3]}
        password : {row[4]}
        """)

    else:
        print(colored(f"Records for {site} don't exist! ", 'red'))



def retrieve_saved_passwords(find_website = ''):
    global connection, cur

    connection = sqlite3.connect('database.sqlite3')
    cur = connection.cursor()
    
    find_website = input("Enter the website (press enter to view all records): ")

    if len(find_website) < 1:
        find_all()

    else:
        find_record(find_website)

    cur.close()