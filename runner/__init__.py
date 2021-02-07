# This is free software licensed under the MIT license.
# Copyright (c) 2021 Samarth Ramesh <samarthr1@outlook.com>
# You should have recived a copy of the MIT license with this file.
# In case you have not, visit https://github.com/samarth-ramsh/mtlaucher


import os
import platform
import random
import sqlite3
import subprocess
import sys
import traceback
import hashlib
import pathlib

import sessionVars
from authentication import auth
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QListWidgetItem


def run(engname, rargs: list):
    if not os.path.isdir(os.path.join(os.getcwd(), 'runner', engname)):
        return False, 'Engine Not Found'
    else:
        if not os.path.isfile(os.path.join(os.getcwd(), 'runner', engname, 'bin', 'minetest')):
            return False, 'Engine Not Found'
        else:
            engpath = os.path.join(
                os.getcwd(), 'runner', engname, 'bin', 'minetest')

    subprocess.Popen(list([engpath, ] + rargs))


def isEng(f):
    # linux-> l windows -> w . Used to determine OS
    pC = platform.system()[0].lower()
    if f.name[0] == 'e' and f.name[1] == pC:
        return 1
    else:
        return 0


def getEngs():
    return [f.name for f in os.scandir(os.path.join(os.getcwd(), 'runner')) if isEng(f)]


def mkPass(uname):
    unameS = uname + str(random.randint(1, 100))
    unameLS = list(unameS)
    random.shuffle(unameLS)
    return (''.join(unameLS))


def showException(e):
    dlg_file = QFile('views/decrypt_error.dialog.ui')
    lder = QUiLoader()
    dlg = lder.load(dlg_file)

    tb = e.__traceback__
    x = '\n'.join(traceback.format_exception(e, e, tb))
    ql = QListWidgetItem()
    ql.setText(str(x))
    # print(x)
    dlg.lw.addItem(ql)

    # error handling->show traceback, then exit

    dlg.exec_()
    sys.exit(1)


def getPass(uname, port, addr):

    conn = sqlite3.connect(os.path.join(
        pathlib.Path().home(), '.config', 'mtclient', 'database.sqlite3'))

    cur = conn.cursor()
    uid = auth.getUid(addr, port, uname)

    cur.execute('SELECT passwd, iv FROM passwds WHERE uid = ?', (uid, ))

    dbVal = cur.fetchone()
    conn.close()
    if dbVal:
        try:
            rv = auth.decryptPayload(bytes(
                sessionVars.password, encoding='UTF-8'),
                auth.getSalt(uname, addr, port),
                bytes.fromhex(dbVal[1]), bytes.fromhex(dbVal[0]))

            # print(rv)
            return rv
        except Exception as e:
            showException(e)


def savePasswd(addr, port, uname, passwd):
    iv = os.urandom(8)
    try:
        passToken = auth.encryptPayload(bytes(sessionVars.password,
                                              encoding='UTF-8'),
                                        auth.getSalt(uname, addr, port),
                                        iv,
                                        bytes(passwd, encoding='UTF-8'))
    except Exception as e:
        showException(e)

    uid = auth.getUid(addr, port, uname)

    conn = sqlite3.connect(os.path.join(
        pathlib.Path().home(), '.config', 'mtclient', 'database.sqlite3'))

    cur = conn.cursor()

    cur.execute('INSERT INTO passwds(addr, port, uname, passwd, iv, uid)\
    		VALUES (?, ?, ?, ?, ?, ?)',
                (addr, port, uname, passToken.hex(), iv.hex(), uid))

    conn.commit()
    conn.close()
    #print('saved Password')


def showAskPass(uname: str, addr: str, port: str, passwd: str):
    dlg_file = QFile('views/savepasswd.dialog.ui')
    lder = QUiLoader()
    dlg = lder.load(dlg_file)
    dlg.addr.setText(f'{addr} :{port}')
    dlg.user.setText(f'and user {uname}')
    #print(addr, port, uname, passwd)
    dlg.accepted.connect(lambda: savePasswd(addr, port, uname, passwd))
    dlg.exec_()


def intiate(addr, port, uname, engName, passIn, noIgnorePass, win):

    if noIgnorePass:
        passwd = (passIn, None,)[0]
        showAskPass(uname, addr, port, passwd)
    else:
        passwd = getPass(uname, port, addr)
        if not passwd:
            savePasswd(addr, port, uname, mkPass(uname))

    confPath = os.path.join(os.getcwd(), 'assets', 'config', 'mtclient.conf')

    args = ['--go',
            '--config {}'.format(confPath),
            '--address {}'.format(addr),
            '--port "{}"'.format(port),
            '--password {}'.format(passwd),
            '--name {}'.format(uname)]

    args = ' '.join(args)
    # print(args)
    args = args.split(' ')
    run(engName, args)
