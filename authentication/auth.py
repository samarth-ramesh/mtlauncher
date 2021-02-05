# This is free software licensed under the MIT license.
# Copyright (c) 2021 Samarth Ramesh <samarthr1@outlook.com>
# You should have recived a copy of the MIT license with this file. In case you ahve not, visit https://github.com/samarth-ramsh/mtlaucher


import hashlib
import sqlite3
import os
import pathlib

from Crypto.Cipher import ChaCha20
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512


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


def encryptPayload(passwd: bytes, salt: bytes, iv: bytes, payload: bytes):
    key = PBKDF2(password=passwd, salt=salt, hmac_hash_module=SHA512, dkLen=32)
    cipher = ChaCha20.new(key=key, nonce=iv)
    return cipher.encrypt(payload)


def decryptPayload(passwd: bytes, salt: bytes, iv: bytes, payload: bytes):
    key = PBKDF2(password=passwd, salt=salt, hmac_hash_module=SHA512, dkLen=32)
    cipher = ChaCha20.new(key=key, nonce=iv)
    return cipher.decrypt(payload)


def getSalt(uname: str, addr: str, port: str):
    return hashlib.sha256(bytes((uname+addr+port), encoding='UTF-8')).digest()