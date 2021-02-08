# This is free software licensed under the MIT license.
# Copyright (c) 2021 Samarth Ramesh <samarthr1@outlook.com>
# You should have recived a copy of the MIT license with this file.
# In case you have not, visit https://github.com/samarth-ramsh/mtlaucher.

# This Python file uses
#  following encoding: utf-8
import sys
import os
import pathlib

if __name__ == '__main__':
    os.chdir(pathlib.Path(__file__).parent.absolute())

from authentication import auth
from styles import compile
import runner
import sessionVars

from PySide2.QtWidgets import QApplication, QGraphicsScene
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, QUrl
from PySide2.QtSvg import QGraphicsSvgItem
from PySide2.QtGui import QPixmap, QIcon


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
            sessionVars.password = passwd
            sessionVars.username = uname

            changeWidgetToGo(win, uname)


def showPass(win):
    if win.centralWidget().showPass.isChecked():
        win.centralWidget().passwd.show()
        win.centralWidget().passwdIn.show()
    else:
        win.centralWidget().passwd.hide()
        win.centralWidget().passwdIn.hide()


def changeWidgetToGo(win, uname):
    ui_file = QFile(str(sessionVars.viewPath / "go.widget.ui"))
    ui_file.open(QFile.ReadOnly)

    lder = QUiLoader()

    dlg = lder.load(ui_file)

    win.centralWidget().hide()
    win.setCentralWidget(dlg)

    engs = runner.getEngs()
    pxmp = QPixmap(str(sessionVars.assetPath / 'icon.png'), format="png")
    icn = QIcon(pxmp)
    for engine in engs:
        win.centralWidget().engines.addItem(icn, engine)

    win.centralWidget().passwd.hide()
    win.centralWidget().passwdIn.hide()

    win.centralWidget().uname.setText(uname)
    win.centralWidget().port.setText('30000')
    win.centralWidget().addr.setText('nri.edgy1.net')

    win.centralWidget().go.clicked.connect((lambda:runner.intiate(
                                            win.centralWidget().addr.text(),
                                            win.centralWidget().port.text(),
                                            win.centralWidget().uname.text()
                                            ,win.centralWidget().engines.
                                        		currentText(),
                                            win.centralWidget().passwdIn.
                                            	text(),
                                            win.centralWidget().showPass
                                            	.isChecked(), 
                                            win)
    ))

    win.centralWidget().showPass.stateChanged.connect(lambda: showPass(win))

    showLogo(win.centralWidget(), 'minetest_logo.svg')


def showLogo(win, logoName):

    logoPath = str(sessionVars.assetPath / logoName)

    ico = QGraphicsSvgItem(logoPath)
    scene = QGraphicsScene()
    scene.addItem(ico)

    win.logo.setScene(scene)


def getJoinHelp():

    ui_file = QFile(str(sessionVars.viewPath / "help.ui"))
    ui_file.open(QFile.ReadOnly)

    lder = QUiLoader()
    dlg = lder.load(ui_file)

    resUrl = QUrl(str(sessionVars.helpPath / 'signon.md'))
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

    if len(uname) > 20:
        win.centralWidget().eMesg.setText(
            f'Error, UserName too long. \n{len(uname)} > 20')
        return None

    if any(char in list(sessionVars.whitespace) for char in uname):
        win.centralWidget().eMesg.setText(
            f'Error. Username contains whitespace')

    if passwd == uname:
        win.centralWidget().eMesg.setText(
            'Error, Cannot have UserName == Password')
        return None

    succsess, error = auth.addUser(uname, passwd)
    if not succsess:
        win.centralWidget().eMesg.setText(error)
    else:
        changeWidgetToGo(win, uname)


def initNscreen(stylesheets):
    app = QApplication([])
    app.setStyleSheet(stylesheets)

    ui_file = QFile(str(sessionVars.viewPath / "main.ui"))
    ui_file.open(QFile.ReadOnly)
    wdg_file = QFile(str(sessionVars.viewPath / "start.widget.ui"))

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

def initRscreen(stylesheets):

    app = QApplication([])
    app.setStyleSheet(stylesheets)

    ui_file = QFile(str(sessionVars.viewPath / "main.ui"))
    ui_file.open(QFile.ReadOnly)
    wdg_file = QFile(str(sessionVars.viewPath / "login.widget.ui"))
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


if __name__ == "__main__":
    stylesheets = compile()
    if os.path.isfile(os.path.join(pathlib.Path().home(),
                                   '.config',
                                   'mtclient',
                                   'database.sqlite3')):
        print('using old db')
        initRscreen(stylesheets)
    else:
        print('using new db')
        initNscreen(stylesheets)
