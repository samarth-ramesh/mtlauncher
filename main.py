# This Python file uses 
#  following encoding: utf-8
import sys
import os

from authentication import auth
from styles import compile

from PySide2.QtWidgets import QApplication, QGraphicsScene
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QUrl
from PySide2.QtSvg import QGraphicsSvgItem


def runMT(addr, passwd, uname):
    os.system('minetest --config "assets/config/mtclient.conf" --go --name "{}" --password "{}" --address "{}"'.format(uname, passwd, addr))

def login(win):
    passwd = win.centralWidget().passwd.text()
    uname = win.centralWidget().username.text()
    if not (passwd and uname):
        win.centralWidget().elabel.setText('Expected UserName & Password')
    else:
        win.centralWidget().elabel.setText('')
        state, errMsg = auth.checkLogin(passwd, uname)
        if not state:
            with open(errMsg, 'r') as fp:
                win.centralWidget().elabel.setText(fp.read())
        else:
            changeWidgetToGo(win, uname)
            

def changeWidgetToGo(win, uname):
    ui_file = QFile("views/go.widget.ui")
    ui_file.open(QFile.ReadOnly)
    
    lder = QUiLoader()
    winNext = lder.load(ui_file)
    win.centralWidget().hide()
    win.setCentralWidget(winNext)
    showLogo(win.centralWidget(), 'minetest_logo.svg')
    win.centralWidget().uname.setText(uname)


def showLogo(win, logoName):
    logoPath = os.path.join('assets' , logoName)
    ico = QGraphicsSvgItem(logoPath)
    scene = QGraphicsScene()
    scene.addItem(ico)
    win.logo.setScene(scene)
    
def getJoinHelp():
    
    ui_file = QFile("views/help.ui")
    ui_file.open(QFile.ReadOnly)
    
    lder = QUiLoader()
    dlg = lder.load(ui_file)
    
    resUrl = QUrl('assets/helptext/signon.md')
    dlg.help_text.setSource(resUrl)

    dlg.exec_()

def initUser(win):
    uname = win.centralWidget().uname.text()
    passwd = win.centralWidget().passwd.text()
    cpasswd = win.centralWidget().cpasswd.text()

    if not passwd == cpasswd:
        win.centralWidget().eMesg.setText('Error. Passwords dont match')
        return None

    if not len(passwd):
        win.centralWidget().eMesg.setText('Error. Password must not be empty')
        return None
    
    if not len(uname):
        win.centralWidget().eMesg.setText('Error, Cannot have empty UserName')
        return None
    
    succsess, error = auth.addUser(uname, passwd)
    if not succsess:
        win.centralWidget().eMesg.setText(error)
        print(error)
    
    else:
        changeWidgetToGo(win, uname)
        
        

def initRscreen(stylesheets):
    
    app = QApplication([])
    app.setStyleSheet(stylesheets)
    # ...
    
    ui_file = QFile("views/main.ui")
    ui_file.open(QFile.ReadOnly)
    wdg_file = QFile("views/login.widget.ui")
    wdg_file.open(QFile.ReadOnly)

    lder = QUiLoader()
    
    win = lder.load(ui_file)
    wdg = lder.load(wdg_file)
    
    win.setCentralWidget(wdg)
    
    showLogo(win.centralWidget(), 'minetest_logo.svg')
    
    win.centralWidget().usernamesubmit.clicked.connect(lambda: login(win))

    win.show()
    app.exec_()
    
    sys.exit(0)


def initNscreen(stylesheets):
    app = QApplication([])
    app.setStyleSheet(stylesheets)

    ui_file = QFile("views/main.ui")
    ui_file.open(QFile.ReadOnly)
    wdg_file = QFile("views/start.ui")

    lder = QUiLoader()
    
    win = lder.load(ui_file)
    wdg = lder.load(wdg_file)

    win.setCentralWidget(wdg)

    showLogo(win.centralWidget(), 'minetest_logo.svg')
    win.centralWidget().help.clicked.connect(lambda: getJoinHelp())
    win.centralWidget().go.clicked.connect(lambda: initUser(win))
    auth.runSetup()

    win.show()
    app.exec_()
    sys.exit(0)

if __name__ == "__main__":
    stylesheets = compile()
    if os.path.isfile(os.path.join(os.getenv('HOME'), '.config', 'mtclient', 'database.sqlite3')):
        initRscreen(stylesheets)
    else:
        initNscreen(stylesheets)