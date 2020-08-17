import sqlite3
from termcolor import colored
from helpers import email_validator, isWebsiteUnique


def update_record(old_website, record):
    # record is a list as a tuple object does not support assignment

    cur.execute("SELECT * FROM Passwords WHERE website = ?", (old_website,))

    row = cur.fetchone()
    _id = row[0]
    # row = (_id, website, email, username, password)

    for i in range(len(record)):
        if len(record[i]) < 1:
            record[i] = row[i + 1]

    cur.execute("""
        UPDATE Passwords
        set website = ?,
        email = ?,
        username = ?,
        password = ?
        WHERE _id = ?
    """, (record[0], record[1], record[2], record[3], _id))

    connection.commit()

    print(colored("Updated Successfully", 'green'))


def update_a_password(website):
    global connection, cur
    connection = sqlite3.connect('database.sqlite3')
    cur = connection.cursor()

    cur.execute("SELECT * FROM Passwords WHERE website = ?", (website,))

    row = cur.fetchone()

    if row is not None:
        print(colored(f"Update records for {website} \n* Required", 'blue'))
        print(colored("\nPlease enter new values for the fields" 
                        "\nLeave blank to not update\n", 'blue'))
        
        new_website = input("Website : ")

        if len(new_website) > 1:
            while not isWebsiteUnique(new_website):
                print(colored("An entry with the current website name already exists!", 'red'))
                new_website = input("Website : ")


        new_username = input("Username : ")

        new_email = input("Email : ")

        if len(new_email) >= 1:
            while not email_validator(new_email):
                print(colored("\nThe email entered is invalid. Please enter a valid email.", 'red'))
                new_email = input("Enter Email: ")


        new_password = input("Password* : ")
        
        new_password_conf = input("Password (again)* : ")

        if new_password == new_password_conf:
            update_record(website, [new_website, new_email, new_username, new_password])

        else:
            print(colored("Passwords do not match", 'red'))


    else:
        print(colored(f"Records for '{website}' don't exist", 'red'))


    cur.close()