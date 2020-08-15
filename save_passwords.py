import sqlite3
import re
from termcolor import colored


connection = sqlite3.connect('database.sqlite3')
cur = connection.cursor()

def email_validator(mailaddress):
    pattern = r'^([a-zA-Z0-9\.\-_]+)@[a-zA-Z_\-]{2,}\.[a-z\-_]{2,}'

    if re.search(pattern, mailaddress):
        return True

    return False


def isWebsiteUnique(site):
    cur.execute("SELECT * FROM Passwords WHERE website = ?", (site,))

    if cur.fetchone() is None:
        return True

    else:
        return False


def save_a_password():
    website = ''
    email = ''
    username = ''
    password = ''
    p_confirm = ''

    website = input("Website Name : ").lower()


    email = input("Enter Email: ")

    if len(email) >= 1:
        while not email_validator(email):
            print(colored("\nThe email entered is invalid. Please enter a valid email.", 'red'))
            email = input("Enter Email: ")

    username = input("Enter Username: ")

    password = input("Enter Password: ")

    p_confirm = input("Confirm Password: ")

    if password == p_confirm:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Passwords (
                website TEXT UNIQUE PRIMARY KEY NOT NULL, 
                email TEXT, 
                username TEXT, 
                password TEXT NOT NULL
            )
        """)

        if len(username) < 1 and len(email) < 1:
            print(colored("\nUsername and Email both cannot be empty", 'red'))
            print(colored("Record not saved!", 'red'))
            return

        if not isWebsiteUnique(website):
            print(colored("An entry with the current website name already exists!", 'red'))
            print("Do you want to Update it? (Y/N)")

            # CALL A FUNCTION TO UPDATE THE RECORD IF INPUT IS YES

        else:
            cur.execute("""
                INSERT INTO Passwords (website, email, username, password)
                VALUES (?, ?, ?, ?) 
            """, (website, email, username, password))

            connection.commit()

            print(colored("Saved Successfully!", 'green'))

    else:
        print(colored("Passwords do not match! ", 'red'))