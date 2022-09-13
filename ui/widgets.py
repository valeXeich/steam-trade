import logging
import requests
from core.launch import Start
from PyQt5 import QtWidgets, QtCore, QtGui


class Sidebar:
    test = False

    def __init__(self, parent, user, session) -> None:
        with open('steam-trade/ui/css/sidebar.css') as style:
            self.styles = style.read()
        self.sidebar = QtWidgets.QWidget(parent)
        self.session = session
        self.user = user
        self.sidebar.setGeometry(QtCore.QRect(0, 0, 181, 721))
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet(self.styles)
        self.buttons_box()
        self.buttons()
        self.avatar()
        self.username()

    def buttons_box(self):
        self.buttons_area = QtWidgets.QFrame(self.sidebar)
        self.buttons_area.setGeometry(QtCore.QRect(0, 60, 181, 191))
        self.buttons_area.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttons_area.setFrameShadow(QtWidgets.QFrame.Raised)
        self.buttons_area.setObjectName('buttons_area')
        return self.buttons_area
    
    def buttons(self):
        self.table_button = QtWidgets.QPushButton(self.buttons_area)
        self.table_button.setGeometry(QtCore.QRect(0, 0, 181, 41))
        self.table_button.setObjectName("active-btn")
        self.table_button.setText('Table')

        self.log_button = QtWidgets.QPushButton(self.buttons_area)
        self.log_button.setGeometry(QtCore.QRect(0, 40, 181, 41))
        self.log_button.setObjectName("un-active-btn")
        self.log_button.setText('Logs')

        self.settings_button = QtWidgets.QPushButton(self.buttons_area)
        self.settings_button.setGeometry(QtCore.QRect(0, 80, 181, 41))
        self.settings_button.setObjectName("un-active-btn")
        self.settings_button.setText('Settings')

        self.start_button = QtWidgets.QPushButton(self.sidebar)
        self.start_button.setText('ON')
        self.start_button.setGeometry(QtCore.QRect(0, 10, 181, 41))
        self.start_button.setObjectName('btn-on')
        self.launch = Start(self.session)
        self.start_button.clicked.connect(self.switch)
        
    def switch(self):
        self.test = not self.test
        if not self.launch.isRunning():
            self.start_button.setObjectName('btn-off')
            self.start_button.setText('OFF')
            self.start_button.setStyleSheet(self.styles)
            self.launch.start()
        else:
            self.start_button.setObjectName('btn-on')
            self.start_button.setText('ON')
            self.start_button.setStyleSheet(self.styles)
            self.launch.stop()

    def avatar(self):
        self.avatar = QtGui.QImage()
        self.avatar.loadFromData(requests.get(self.user.avatar).content)
        self.avatar_lbl = QtWidgets.QLabel(self.sidebar)
        self.avatar_lbl.setGeometry(QtCore.QRect(10, 669, 41, 41))   
        self.avatar_lbl.setPixmap(QtGui.QPixmap(self.avatar))
        self.avatar_lbl.setScaledContents(True)  
    
    def username(self):
        self.username = QtWidgets.QLabel(self.sidebar)
        self.username.setGeometry(QtCore.QRect(60, 680, 67, 17))
        self.username.setObjectName("username")
        self.username.setText(self.user.account_name)
    

class QTextEditLogger(logging.Handler, QtCore.QObject):
    appendPlainText = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.appendPlainText.connect(self.widget.appendPlainText)

        
    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return 
 