import hashlib
import sqlite3
import os
from sqlite3.dbapi2 import DatabaseError, connect

def checkLogin(passwd, login):
    conn = sqlite3.connect(os.path.join(os.getenv('HOME'), '.config', 'mtclient', 'database.sqlite3'))
    inp = hashlib.pbkdf2_hmac('sha256', bytes(passwd, 'UTF-8'), b'lah di dah, a very strong salt', 10000)
    cur = conn.cursor()
    cur.execute("SELECT passwd FROM users WHERE username = ?", (login, ))
    try:
        if not inp.hex() == cur.fetchone()[0]:
            return (0, "assets/helptext/inc_passwd.md")
        else:
            return (1, None)
    except(TypeError, IndexError):
        return (0, "assets/helptext/passwd_error.md")

def runSetup():
    try:
        os.makedirs(os.path.join(os.getenv('HOME'), '.config', 'mtclient'))
    except(FileExistsError):
        pass
    except:
        raise
    conn = sqlite3.connect(os.path.join(os.getenv('HOME'), '.config', 'mtclient', 'database.sqlite3'))
    cur = conn.cursor()
    with open('assets/sql/init.sql', 'r') as fp:
        for statement in fp:
            cur.execute(statement)
        conn.commit()
    conn.close()
    print('Loaded Database')

def addUser(uname, passwd):
    inp = hashlib.pbkdf2_hmac('sha256', bytes(passwd, 'UTF-8'), b'lah di dah, a very strong salt', 10000)
    
    try:
        conn = sqlite3.connect(os.path.join(os.getenv('HOME'), '.config', 'mtclient', 'database.sqlite3'))
        cur = conn.cursor()
        cur.execute("INSERT INTO users(username, passwd) VALUES (?, ?)", (uname, inp.hex(), ))
        conn.commit()
        print('added user')
    except(sqlite3.IntegrityError):
        return (False, "Username already exists")
    except(sqlite3.DatabaseError) as e:
        raise(e)
        #return (False, "Database error.")
    try:
        conn.close()
    except:
        pass
    return True, None