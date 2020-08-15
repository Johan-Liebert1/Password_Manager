import sqlite3
import hashlib
from termcolor import colored

from save_passwords import save_a_password
from get_passwords import retrieve_saved_passwords

connection = sqlite3.connect('database.sqlite3')
cur = connection.cursor()


def create_new_admin():
    print(colored("\nCREATE NEW ADMIN\n", 'blue', attrs=['bold']))
    admin_username = input("Enter Username: ")
    admin_password = input("Enter Password: ")
    password_conf  = input("Enter Password (again): ")
    salt = ''

    if admin_password == password_conf:
        hashed_password = hashlib.sha256(admin_password.encode()).hexdigest()

        # also need to add a salt field

        cur.execute("""
            INSERT INTO Admin 
                (admin, salt, password)
                VALUES (?, ?, ?)
        """, (admin_username, salt, hashed_password))

        connection.commit()

    else:
        print(colored('Passwords do not match', 'red'))

    cur.close()


def admin_login():
    print(colored("\nLOG IN\n", 'blue', attrs=['bold']))
    admin_username = input("Enter Admin Username: ")

    cur.execute("SELECT * FROM Admin WHERE admin = ?", (admin_username,))

    row = cur.fetchone()

    if row is not None:
        hashed_password = row[2]
        passwrd = input("Enter your Password: ")

        if hashlib.sha256(passwrd.encode()).hexdigest() == hashed_password:
            print(colored("Logged you in successfully! ", 'green'))

            what_to_do_next()
    
    else:
        print(colored(f"Admin with username = {admin_username} not found!", 'red'))

    cur.close()



def what_to_do_next():
    more = 'y'

    while True and more.lower() == 'y':
        inp = input("\n1. View Stored Passwords (v/V/view)" 
                    "\n2. Add new Passwords (a/A/add)" 
                    "\n3. Exit (e/E/exit)\n")

        possible_inputs = ['v', 'view', 'a', 'add', 'e', 'exit']

        if inp.lower() not in possible_inputs:
            print(colored("Please enter a valid option!", 'red'))
            return

        elif inp.lower() in possible_inputs[0:2]:
            retrieve_saved_passwords()
            
        elif inp.lower() in possible_inputs[2:4]:
            save_a_password()

        elif inp.lower() in possible_inputs[4:]:
            print("Exiting...")
            break

        more = input("\nDo more stuff? (Y/N): ")

        if more.lower() != 'y':
            print(colored("Exiting...\n", "blue"))
            break

        else:
            continue



def main():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Admin (
            admin TEXT UNIQUE,
            salt TEXT, 
            password TEXT
        );
    """) 

    cur.execute("SELECT * FROM Admin")
    row = cur.fetchone()

    if row is not None:
        admin_login()

    else:
        create_new_admin()

if __name__ == "__main__":
    main()


