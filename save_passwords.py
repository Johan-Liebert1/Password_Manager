import sqlite3
from termcolor import colored

connection = sqlite3.connect('database.sqlite3')
cur = connection.cursor()

def save_a_password():
    website = ''
    email = ''
    username = ''
    password = ''
    p_confirm = ''

    website = input("Website Name : ").lower()

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

        cur.execute("""
            INSERT INTO Passwords (website, email, username, password)
            VALUES (?, ?, ?, ?) 
        """, (website, email, username, password))

        connection.commit()

        print(colored("Saved Successfully!", 'green'))

    else:
        print(colored("Passwords do not match! ", 'red'))