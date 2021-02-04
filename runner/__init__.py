import subprocess, os, sqlite3, random, platform, sys, traceback

from PySide2.QtCore import QProcess, QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QListWidgetItem

from authentication import auth
import sessionVars

def run(engname, rargs: list):
    if not os.path.isdir(os.path.join(os.getcwd(), 'runner', engname)):
        return False, 'Engine Not Found'
    else:
        if not os.path.isfile(os.path.join(os.getcwd(), 'runner', engname, 'bin', 'minetest')):
            return False, 'Engine Not Found'
        else:
            engpath = os.path.join(os.getcwd(), 'runner', engname, 'bin', 'minetest')
    
    subprocess.Popen(list([engpath,] + rargs))


def isEng(f):
    pC = platform.system()[0].lower() # linux-> l windows -> w . Used to determine OS
    if f.name[0] == 'e' and f.name[1] == pC:
        return 1
    else:
        return 0


def getEngs():
    return  [ f.name for f in os.scandir(os.path.join(os.getcwd(), 'runner')) if isEng(f) ]


def mkPass(uname):
    unameS = uname + str(random.randint(1,100))
    unameLS = list(unameS)
    random.shuffle(unameLS)
    return (''.join(unameLS))


def showException(e):
    dlg_file = QFile('views/decrypt_error.dialog.ui')
    lder = QUiLoader()
    dlg = lder.load(dlg_file)

    tb = e.__traceback__
    x= '\n'.join(traceback.format_exception(e,e,tb))
    ql = QListWidgetItem()
    ql.setText(str(x))
    print(x)
    dlg.lw.addItem(ql) 

    ## error handling->show traceback, then exit

    dlg.exec_()
    sys.exit(1)


def getPass(uname, port, addr):
    conn = sqlite3.connect(os.path.join(os.getenv('HOME'), '.config', 'mtclient', 'database.sqlite3'))
    cur = conn.cursor()
    
    cur.execute('SELECT passwd FROM passwds WHERE (((uname = ?) AND (addr = ?)) AND (port = ?))', (uname, addr, port))
    dbVal = cur.fetchone()
    conn.close()
    if dbVal:
        try:
            return auth.decryptPayload(bytes(sessionVars.password, encoding='UTF-8'), auth.getSalt(uname, addr, port), bytes(dbVal[0], encoding='UTF-8'))
        except Exception as e:
            showException(e)
            



def savePasswd(addr, port, uname, passwd):
    try:
        passToken = auth.encryptPayload(bytes(sessionVars.password, encoding='UTF-8'), auth.getSalt(uname, addr, port), bytes(passwd, encoding='UTF-8'))
    except Exception as e:
        showException(e)
    
    conn = sqlite3.connect(os.path.join(os.getenv('HOME'), '.config', 'mtclient', 'database.sqlite3'))
    cur = conn.cursor()
    cur.execute('INSERT INTO passwds(addr, port, uname, passwd) VALUES (?, ?, ?, ?)', (addr, port, uname, passToken))
    conn.commit()
    conn.close()
    print('saved Password')

def showAskPass(uname: str, addr: str, port: str, passwd: str):
    dlg_file = QFile('views/savepasswd.dialog.ui')
    lder = QUiLoader()
    dlg = lder.load(dlg_file)
    dlg.addr.setText(f'{addr} :{port}')
    dlg.user.setText(f'and user {uname}')
    print(addr, port, uname, passwd)
    dlg.accepted.connect(lambda: savePasswd(addr, port, uname, passwd))
    dlg.exec_()


def intiate(addr, port, uname, engName, passIn, noIgnorePass, win):
    
    if noIgnorePass:
        passwd = (passIn,None,)[0]
        showAskPass(uname, addr, port, passwd)
    else:
        passwd = getPass(uname, port, addr)
        if not passwd:
            savePasswd(addr, port, uname, mkPass(uname))
    
    confPath = os.path.join(os.getcwd(), 'assets', 'config', 'mtclient.conf')

    args = ['--go', '--config {}'.format(confPath), '--address {}'.format(addr), '--port "{}"'.format(port), '--password {}'.format(passwd), '--name {}'.format(uname)]
    args = ' '.join(args)
    print(args)
    args = args.split(' ')
    run(engName, args)
