import hashlib
import sqlite3
import os
import pathlib
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

def checkLogin(passwd, login):
    conn = sqlite3.connect(os.path.join(pathlib.Path().home(), '.config', 'mtclient', 'database.sqlite3'))
    inp = hashlib.pbkdf2_hmac('sha256', bytes(passwd, 'UTF-8'), b'lah di dah, a very strong salt', 100000)
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
        os.makedirs(os.path.join(pathlib.Path().home(), '.config', 'mtclient'))
    except(FileExistsError):
        pass
    except Exception as e:
        raise(e)
    conn = sqlite3.connect(os.path.join(pathlib.Path().home(), '.config', 'mtclient', 'database.sqlite3'))
    cur = conn.cursor()
    with open('assets/sql/init.sql', 'r') as fp:
        for statement in fp:
            cur.execute(statement)
        conn.commit()
    conn.close()
    print('Loaded Database')

def addUser(uname, passwd):
    inp = hashlib.pbkdf2_hmac('sha256', bytes(passwd, 'UTF-8'), b'lah di dah, a very strong salt', 100000)
    
    try:
        conn = sqlite3.connect(os.path.join(pathlib.Path().home(), '.config', 'mtclient', 'database.sqlite3'))
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

def encryptPayload(passwd: bytes, salt: bytes, payload: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(passwd))
    f = Fernet(key)
    print(f.encrypt(payload).decode(encoding='UTF-8'))
    return f.encrypt(payload).decode(encoding='UTF-8')

def decryptPayload(passwd: bytes, salt: bytes, token: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(passwd))
    f = Fernet(key)
    return (f.decrypt(token)).decode(encoding='UTF-8')

def getSalt(uname: str, addr: str, port: str):
    return hashlib.sha256(bytes((uname+addr+port), encoding='UTF-8')).digest()