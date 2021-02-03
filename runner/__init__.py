import subprocess, os, sqlite3, random

from PySide2.QtCore import QProcess

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
    if f.name[0] == 'e':
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

def intiate(addr, port, uname, engName, passIn, noIgnorePass):
    if noIgnorePass:
        passwd = (passIn,None,)
    else:
        conn = sqlite3.connect(os.path.join(os.getenv('HOME'), '.config', 'mtclient', 'database.sqlite3'))
        cur = conn.cursor()
        
        cur.execute('SELECT passwd FROM passwds WHERE (((uname = ?) AND (addr = ?)) AND (port = ?))', (uname, addr, port))
        dbVal = cur.fetchall()
        if dbVal:
            passwd = dbVal[0]
        else:
            passwd = mkPass(uname)
            cur.execute('INSERT INTO passwds(addr, port, uname, passwd) VALUES (?, ?, ?, ?)', (addr, port, uname, passwd))
            conn.commit()
    
    confPath = os.path.join(os.getcwd(), 'assets', 'config', 'mtclient.conf')

    args = ['--go', '--config {}'.format(confPath), '--address {}'.format(addr), '--port "{}"'.format(port), '--password "{}"'.format(passwd), '--name {}'.format(uname)]
    args = ' '.join(args)
    print(args)
    args = args.split(' ')
    run(engName, args)
