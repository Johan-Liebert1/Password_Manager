import sqlite3
from termcolor import colored
from helpers import email_validator, isWebsiteUnique
from update_passwords import update_a_password


def save_a_password():
    global connection, cur
    connection = sqlite3.connect('database.sqlite3')
    cur = connection.cursor()

    website = ''
    email = ''
    username = ''
    password = ''
    p_confirm = ''

    print(colored("\n* Required", 'blue'))

    website = input("Website Name* : ").lower()

    while len(website) < 1:
        print(colored("Please enter a valid website", 'red'))
        website = input("Website Name* : ").lower()

    
    if not isWebsiteUnique(website):
        print(colored("An entry with the current website name already exists!", 'red'))
        
        update_or_not = input("Do you want to Update it's records? (Y/N) ")

        if update_or_not.lower() == 'y':
            update_a_password(website)

        else:
            cur.close()
            return

    email = input("Enter Email : ")

    if len(email) >= 1:
        while not email_validator(email):
            print(colored("\nThe email entered is invalid. Please enter a valid email.", 'red'))
            email = input("Enter Email : ")

    username = input("Enter Username : ")

    password = input("Enter Password* : ")

    p_confirm = input("Confirm Password* : ")

    if password == p_confirm:

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Passwords (
                _id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                website TEXT UNIQUE NOT NULL, 
                email TEXT, 
                username TEXT, 
                password TEXT NOT NULL
            )
        """)
        connection.commit()

        if len(username) < 1 and len(email) < 1:
            print(colored("\nUsername and Email both cannot be empty", 'red'))
            print(colored("Record not saved!", 'red'))
            cur.close()
            return


        else:
            cur.execute("""
                INSERT INTO Passwords (website, email, username, password)
                VALUES (?, ?, ?, ?) 
            """, (website, email, username, password))

            connection.commit()

            print(colored("Saved Successfully!", 'green'))

    else:
        print(colored("Passwords do not match! ", 'red'))

    cur.close()