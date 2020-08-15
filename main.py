import sqlite3
from os import path
from termcolor import colored
import hashlib

connection = sqlite3.connect('admin.sqlite3')
cur = connection.cursor()


def create_new_admin():
    admin_username = input("Enter Username: ")
    admin_password = input("Enter Password: ")
    password_conf  = input("Enter Password (again): ")
    salt = ''

    if admin_password == password_conf:
        hashed_password = hashlib.sha256(admin_password.encode()).hexdigest()

        cur.execute("""
            DROP TABLE IF EXISTS Admin
        """)

        # also need to add a salt field
        cur.execute("""
            CREATE TABLE Admin (
                admin TEXT,
                salt TEXT, 
                password TEXT
            );
        """)

        cur.execute("""
            INSERT INTO Admin 
                (admin, salt, password)
                VALUES (?, ?, ?)
        """, (admin_username, salt, hashed_password))

        connection.commit()

    else:
        print(colored('Passwords do not match', 'red'))


'''
def what_to_do_next():
    more = 'y'
    while True and more.lower() == 'y':
        inp = input("\n1. View Stored Passwords (v/V/view)" 
                    "\n2. Add new Passwords (a/A/add)" 
                    "\n3. Exit (e/E/exit)\n")

        possible_inputs = ['v', 'view', 'a', 'add', 'e', 'exit']

        if inp.lower() not in possible_inputs:
            print("Please enter a valid option!")
            return

        elif inp.lower() in possible_inputs[0:2]:
            get_passwords()
            
        elif inp.lower() in possible_inputs[2:4]:
            save_passwords()

        elif inp.lower() in possible_inputs[4:]:
            print("Exiting...")
            break

        more = input("\nDo more stuff? (Y/N): ")

        if more.lower() != 'y':
            print("Exiting...")
            break

        else:
            continue
'''

if __name__ == "__main__":
    create_new_admin()


