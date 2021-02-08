# This is free software licensed under the MIT license.
# Copyright (c) 2021 Samarth Ramesh <samarthr1@outlook.com>
# You should have recived a copy of the MIT license with this file.
# In case you ahve not, visit https://github.com/samarth-ramsh/mtlaucher


import hashlib
import sqlite3
import os
import pathlib

from Crypto.Cipher import ChaCha20
from Crypto.Protocol.KDF import scrypt


def checkLogin(passwd, login):
    conn = sqlite3.connect(os.path.join(
        pathlib.Path().home(),
        '.config',
        'mtclient',
        'database.sqlite3'))
    inp = hashlib.pbkdf2_hmac('sha256',
                              bytes(passwd, 'UTF-8'),
                              b'lah di dah, a very strong salt',
                              100000)
    cur = conn.cursor()
    cur.execute("SELECT passwd FROM users WHERE username = ?", (login, ))
    helpTextPath = pathlib.Path() / 'assets' / 'helptext'

    try:
        if not inp.hex() == cur.fetchone()[0]:
            return (0, helpTextPath / "inc_passwd.md")
        else:
            return (1, None)
    except(TypeError):
        return (0, helpTextPath / "passwd_error.md")


def runSetup():
    try:
        os.makedirs(os.path.join(
            pathlib.Path().home(), '.config', 'mtclient'))
    except(FileExistsError):
        pass
    except Exception as e:
        raise(e)
    conn = sqlite3.connect(os.path.join(
        pathlib.Path().home(),
        '.config',
        'mtclient',
        'database.sqlite3'))
    cur = conn.cursor()

    sqlPath = pathlib.Path() / 'assets' / 'sql' / 'init.sql'
    with open(sqlPath, 'r') as fp:
        cur.executescript(fp.read())
    conn.close()
    print('Loaded Database')


def getUid(addr, port, uname):
    return hashlib.md5(bytes(str(addr) + str(port) + str(uname),
                             encoding='UTF-8')).hexdigest()


def addUser(uname, passwd):
    inp = hashlib.pbkdf2_hmac('sha256',
                              bytes(passwd, 'UTF-8'),
                              b'lah di dah, a very strong salt',
                              100000)

    try:
        conn = sqlite3.connect(os.path.join(
            pathlib.Path().home(),
            '.config',
            'mtclient',
            'database.sqlite3'))
        cur = conn.cursor()
        cur.execute("INSERT INTO users(username, passwd) VALUES (?, ?)",
                    (uname, inp.hex(), ))
        conn.commit()
        print('added user')

    except(sqlite3.IntegrityError):
        return (False, "Username already exists")
    except(sqlite3.DatabaseError) as e:
        raise(e)
        # return (False, "Database error.")
    try:
        conn.close()
    except:
        pass
    return True, None


def encryptPayload(passwd: bytes, salt: bytes, iv: bytes, payload: bytes):
    key = scrypt(password=passwd, salt=salt, N=(2**14), key_len=32, r=8, p=1)
    #print(key, iv, salt)
    cipher = ChaCha20.new(key=key, nonce=iv)
    rv = cipher.encrypt(payload)
    print(rv)
    return rv


def decryptPayload(passwd: bytes, salt: bytes, iv: bytes, payload: bytes):
    key = scrypt(password=passwd, salt=salt, N=(2**14), key_len=32, r=8, p=1)
    cipher = ChaCha20.new(key=key, nonce=iv)
    rv = cipher.decrypt(payload)
    print(payload)
    # print(rv)
    return rv.decode(encoding='UTF-8')

