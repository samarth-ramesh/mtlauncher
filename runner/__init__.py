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

    cur.execute('SELECT passwd, iv, slt FROM passwds WHERE uid = ?', (uid, ))

    dbVal = cur.fetchone()
    conn.close()
    if dbVal:
        try:
            rv = auth.decryptPayload(
                bytes(sessionVars.password, encoding='UTF-8'),
                bytes.fromhex(dbVal[2]),
                bytes.fromhex(dbVal[1]),
                bytes.fromhex(dbVal[0]))

            # print(rv)
            return rv
        except Exception as e:
            showException(e)


def overWritePass(uname, passwd, port, addr):
    iv = os.urandom(8)
    slt = os.urandom(16)
    try:
        passToken = auth.encryptPayload(bytes(sessionVars.password,
                                              encoding='UTF-8'),
                                        slt,
                                        iv,
                                        bytes(passwd, encoding='UTF-8'))
    except Exception as e:
        showException(e)

    uid = auth.getUid(addr, port, uname)
    conn = sqlite3.connect(os.path.join(
        pathlib.Path().home(), '.config', 'mtclient', 'database.sqlite3'))

    cur = conn.cursor()
    cur.execute('UPDATE passwds SET passwd = ?, iv=?, slt=? WHERE uid = ?',
                (passToken.hex(), iv.hex(), slt.hex(), uid,))


def savePasswd(addr, port, uname, passwd):
    iv = os.urandom(8)
    slt = os.urandom(16)
    try:
        passToken = auth.encryptPayload(bytes(sessionVars.password,
                                              encoding='UTF-8'),
                                        slt,
                                        iv,
                                        bytes(passwd, encoding='UTF-8'))
    except Exception as e:
        showException(e)

    uid = auth.getUid(addr, port, uname)

    conn = sqlite3.connect(os.path.join(
        pathlib.Path().home(), '.config', 'mtclient', 'database.sqlite3'))

    cur = conn.cursor()

    try:
        cur.execute('INSERT INTO passwds(addr, port, uname, passwd, iv, uid, slt)\
                VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (addr, port, uname, passToken.hex(), iv.hex(), uid, slt.hex()))
        conn.commit()
        conn.close()
    except Exception as e:
        conn.rollback()
        conn.close()
        dlg_file = QFile('views/overwritePass.dialog.ui')
        lder = QUiLoader()
        dlg = lder.load(dlg_file)
        dlg.confText.setText('Error\n'
                             + f'You already have a password for {addr}:{port}'
                             + f'and username {uname}\n'
                             + 'Do you wish to overwrite?')
        dlg.accepted.connect(
            lambda: overWritePass(addr, port, uname, passwd))
        dlg.exec_()

    #print('saved Password')


def showAskPass(uname: str, addr: str, port: str, passwd: str):
    dlg_file = QFile(sessionVars.viewPath / 'savepasswd.dialog.ui')
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
            dlg_file = QFile(sessionVars.viewPath / 'notifypass.dialog.ui')
            lder = QUiLoader()

            dlg = lder.load(dlg_file)
            dlg.tbox.setText('Saving password for\n' +
                             f'{uname}@{addr}:{port}\n' +
                             f'as {passwd}.')
            dlg.exec_()

    confPath = sessionVars.assetPath / 'config' / 'mtclient.conf'

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
