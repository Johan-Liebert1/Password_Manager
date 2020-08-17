import re
import sqlite3
import random

conn = sqlite3.connect('database.sqlite3')


def email_validator(mailaddress):
    pattern = r'^([a-zA-Z0-9\.\-_]+)@[a-zA-Z0-9_\-]{2,}\.[a-z\-_]{2,}'

    if re.search(pattern, mailaddress):
        return True

    return False


def isWebsiteUnique(site):
    cur = conn.cursor()

    cur.execute("SELECT * FROM Passwords WHERE website = ?", (site,))

    if cur.fetchone() is None:
        cur.close()
        return True

    else:
        cur.close()
        return False


def return_random_salt(length):
    # range = 48 to 57, 65 to 90, 97 to 122 all included

    chars = """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"""    

    rand_salt = ''

    for _ in range(length):
        chance = random.randrange(1, 4)

        if chance == 1:
            rand_salt += chr(random.randrange(48, 58))

        elif chance == 2:
            rand_salt += chr(random.randrange(65, 90))

        else:
            rand_salt += chr(random.randrange(97, 122))


    return rand_salt


def print_all_websites():
    cur = conn.cursor()

    cur.execute("SELECT website FROM Passwords")

    list_of_rows = cur.fetchall()

    for index, row in enumerate(list_of_rows):
        # as only website name is being retrieved, row only has (website,)

        print(f'{index + 1}. {row[0]}', end = '\t')

        if (index + 1) % 4 == 0:
            print('\n')

     