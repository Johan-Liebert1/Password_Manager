import re
import sqlite3

def email_validator(mailaddress):
    pattern = r'^([a-zA-Z0-9\.\-_]+)@[a-zA-Z_\-]{2,}\.[a-z\-_]{2,}'

    if re.search(pattern, mailaddress):
        return True

    return False


def isWebsiteUnique(site):
    conn = sqlite3.connect('database.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Passwords WHERE website = ?", (site,))

    if cur.fetchone() is None:
        cur.close()
        return True

    else:
        cur.close()
        return False