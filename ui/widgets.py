import logging
from signal import signal
import requests
from core.launch import Start
from PyQt5 import QtWidgets, QtCore, QtGui

from core.guard import SteamGuardTimer
from .modals import AccountSelectModalWindow, ConfirmModalWindow


class Sidebar:
    
    def __init__(self, parent, user, session, guard) -> None:
        with open('steam-trade/ui/css/sidebar.css') as style:
            self.styles = style.read()
        self.parent = parent
        self.sidebar = QtWidgets.QWidget(self.parent)
        self.session = session
        self.user = user
        self.guard = guard
        self.sidebar.setGeometry(QtCore.QRect(0, 0, 181, 721))
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet(self.styles)
        self.buttons_box()
        self.buttons()
        self.avatar()
        self.username()
        if self.user.shared_secret:
            self.steam_guard_code()

    def buttons_box(self):
        self.buttons_area = QtWidgets.QFrame(self.sidebar)
        self.buttons_area.setGeometry(QtCore.QRect(0, 105, 181, 191))
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

        #test

        self.confirmation_button = QtWidgets.QPushButton(self.sidebar)
        self.confirmation_button.setText('Confirmation')
        self.confirmation_button.setGeometry(QtCore.QRect(0, 55, 181, 41))
        self.confirmation_button.setObjectName('confirmation-btn')
        self.confirmation_button.clicked.connect(self.open_confirmation)
    
    def open_confirmation(self):
        self.t = ConfirmModalWindow(self.session)
        self.t.setupUi()
        self.t.show()
    
    def switch(self):
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
        self.username = QtWidgets.QPushButton(self.sidebar)
        self.username.setGeometry(QtCore.QRect(60, 675, 70, 30))
        self.username.setText(self.user.account_name)
        self.username.setStyleSheet('QPushButton {border: 1px solid #25262c; background-color: #25262c; font-size: 14; color: white; padding: 5px; border-radius: 4px;} QPushButton::hover {background-color: #60626e}')
        self.username.clicked.connect(self.select_account)
    
    def select_account(self):
        self.account_select = AccountSelectModalWindow(self.parent.restart)
        self.account_select.setupUi()
        self.account_select.show()
        
    def steam_guard_code(self):
        self.code = QtWidgets.QLabel(self.sidebar)
        self.code.setGeometry(QtCore.QRect(70, 600, 181, 41))
        self.code.setObjectName('code')
        self.code.setText(self.guard.get_code())
        self.code.mouseDoubleClickEvent = self.copy_code_to_clipboard
        
        self.pbar = QtWidgets.QProgressBar(self.sidebar)
        self.pbar.setGeometry(QtCore.QRect(10, 640, 161, 10))
        self.pbar.setMaximum(30)
        self.pbar.setTextVisible(False)

        self.code_timer = SteamGuardTimer(self.guard)
        self.code_timer.counter.connect(self.code_timer_change)
        self.code_timer.start()
               
    def copy_code_to_clipboard(self, event):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.code.text())
        
    def code_timer_change(self, value):
        self.pbar.setValue(value)
        if value == 0:
            self.code.setText(self.guard.get_code())


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


 