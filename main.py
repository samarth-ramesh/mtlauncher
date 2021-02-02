# This Python file uses 
#  following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QGraphicsScene
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtSvg import QGraphicsSvgItem

def checkSignIn(uname, passwd):
    return 1

def login(win):
    passwd = win.passwd.text()
    uname = win.username.text()
    if not (passwd and uname):
        win.elabel.setText('Expected UserName & Password')
    else:
        win.elabel.setText('')
        if not checkSignIn(passwd, uname):
            win.elabel.setText('Invalid Username or password')
        else:
            win.elabel.setText('Signed In!')

def showLogo(win, logoName):
    ico = QGraphicsSvgItem(logoName)
    scene = QGraphicsScene()
    scene.addItem(ico)
    win.logo.setScene(scene)
    

if __name__ == "__main__":
    app = QApplication([])
    # ...
    ui_file = QFile("main.ui")
    ui_file.open(QFile.ReadOnly)
    lder = QUiLoader()
    win = lder.load(ui_file)
    
    showLogo(win, 'minetest_logo.svg')
    win.usernamesubmit.clicked.connect(lambda: login(win))

    win.show()
    app.exec_()
    sys.exit(0)
