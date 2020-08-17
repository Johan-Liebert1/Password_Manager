import sqlite3
import hashlib
from termcolor import colored

from save_passwords import save_a_password
from get_passwords import retrieve_saved_passwords
from update_passwords import update_a_password
from helpers import return_random_salt, print_all_websites

connection = sqlite3.connect('database.sqlite3')
cur = connection.cursor()


def create_new_admin():
    print(colored("\nCREATE NEW ADMIN\n", 'blue', attrs=['bold']))
    admin_username = input("Enter Username: ")
    admin_password = input("Enter Password: ")
    password_conf  = input("Enter Password (again): ")
    salt = return_random_salt(30)

    # len(salt) = 20, len(admin_password) = variable

    encrypted_pass = ''

    for i in range(len(salt)):
        if i < len(admin_password):
            encrypted_pass += salt[i] + admin_password[i]

        else:
            encrypted_pass += salt[i]

    if admin_password == password_conf:
        hashed_password = hashlib.sha256(encrypted_pass.encode()).hexdigest()

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
        salt = row[1]

        passwrd = input("Enter your Password: ")

        encrypted_pass = ''

        for i in range(len(salt)):
            if i < len(passwrd):
                encrypted_pass += salt[i] + passwrd[i]

            else:
                encrypted_pass += salt[i]


        if hashlib.sha256(encrypted_pass.encode()).hexdigest() == hashed_password:
            print(colored("Logged you in successfully! ", 'green'))

            what_to_do_next()

        else:
            print(colored("Incorrect password", 'red'))
    
    else:
        print(colored(f"Admin with username = {admin_username} not found!", 'red'))

    cur.close()



def what_to_do_next():
    more = 'y'

    while True and more.lower() == 'y':
        inp = input("\n1. View Stored Passwords (1/v/V/view)" 
                    "\n2. Add new Passwords (2/a/A/add)" 
                    "\n3. Update a record (3/u/U/update)"
                    "\n4. Create New Admin (4/ create)"
                    "\n5. Exit (5/e/E/exit)\n")

        possible_inputs = [
            'v', 'view', '1', 
            'a', 'add', '2', 
            'u', 'update', '3',
            'create','4',
            '5', 'e', 'exit', 
        ]

        if inp.lower() not in possible_inputs:
            print(colored("Please enter a valid option!", 'red'))
            return

        elif inp.lower() in possible_inputs[0:3]:
            retrieve_saved_passwords()
            
        elif inp.lower() in possible_inputs[3:6]:
            save_a_password()

        elif inp.lower() in possible_inputs[6:9]:
            print(colored("Your saved records", "green"))
            print_all_websites()
            w = input("\nEnter the website for which you wish to update records: ")
            update_a_password(w)

        elif inp.lower() in possible_inputs[9:11]:
            create_new_admin()

        elif inp.lower() in possible_inputs[11:]:
            print(colored("Exiting...\n", 'blue'))
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

    connection.commit()

    cur.execute("SELECT * FROM Admin")

    row = cur.fetchone()

    if row is not None:
        admin_login()

    else:
        create_new_admin()

if __name__ == "__main__":
    main()


