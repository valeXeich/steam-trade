import time

from PyQt5 import QtCore, QtWidgets

from steamlib.client import SteamClient
from core.db.methods import add_user


class AddItemModalWindow(QtWidgets.QMainWindow):
    def setupUi(self):
        with open('steam-trade/ui/css/modals.css') as style:
            styles = style.read()
        self.setObjectName('AddItemModal')
        self.setWindowTitle('Add Item')
        self.setStyleSheet(styles)
        self.resize(488, 121)
        self.button()
        self.input()
    
    def button(self):
        self.btn_add = QtWidgets.QPushButton(self)
        self.btn_add.setGeometry(QtCore.QRect(150, 70, 181, 31))
        self.btn_add.setObjectName("default-btn")
        self.btn_add.setText('Add Item')
    
    def input(self):
        self.item_input = QtWidgets.QLineEdit(self)
        self.item_input.setGeometry(QtCore.QRect(20, 20, 451, 31))
        self.item_input.setPlaceholderText('URL')
        self.item_input.setObjectName("default-input")


class CodeModalWindow(QtWidgets.QMainWindow):
    def __init__(self, client, login_modal_window, main_window):
        super().__init__()
        self.client = client
        self.login_modal_window = login_modal_window
        self.main_window = main_window
    
    def setupUi(self):
        with open('steam-trade/ui/css/modals.css') as style:
            styles = style.read()
        self.setObjectName('Code')
        self.setWindowTitle('Code')
        self.setStyleSheet(styles)
        self.resize(223, 152)
        self.title()
        self.input()
        self.button()
        
    def title(self):
        self.code_title = QtWidgets.QLabel(self)
        self.code_title.setGeometry(QtCore.QRect(-10, 0, 251, 31))
        self.code_title.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.code_title.setObjectName('code-title')
        self.code_title.setText('Enter your code')
        
    def input(self):
        self.code_input = QtWidgets.QLineEdit(self)
        self.code_input.setGeometry(QtCore.QRect(10, 50, 201, 31))
        self.code_input.setObjectName('default-input')
        self.code_input.setPlaceholderText('Code')

    def button(self):
        self.code_btn = QtWidgets.QPushButton(self)
        self.code_btn.setGeometry(QtCore.QRect(40, 100, 151, 31))
        self.code_btn.setObjectName('default-btn')
        self.code_btn.setText('OK')
        self.code_btn.clicked.connect(self.send_code)
        
        
    def send_code(self):
        resp = self.client.login(code=self.code_input.text())
        cookies = resp.cookies.get_dict()
        if cookies.get('sessionid', False):
            add_user(self.client.username, cookies)
            self.close()
            time.sleep(.5)
            self.login_modal_window.close()
            time.sleep(.5)
            self.main_window.setupUi()
            self.main_window.show()
    

class LoginModalWindow(QtWidgets.QMainWindow):
    def __init__(self, main_win):
        super().__init__()
        self.main_win = main_win
    
    def setupUi(self):
        with open('steam-trade/ui/css/modals.css') as style:
            styles = style.read()
        self.setObjectName('Login')
        self.resize(441, 250)
        self.policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.policy.setHorizontalStretch(0)
        self.policy.setVerticalStretch(0)
        self.policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(self.policy)
        self.setWindowTitle('Login')
        self.setStyleSheet(styles)
        self.title()
        self.inputs()
        self.button()

    def inputs(self):
        self.login_input = QtWidgets.QLineEdit(self)
        self.login_input.setGeometry(QtCore.QRect(30, 80, 381, 31))
        self.login_input.setObjectName('default-input')
        self.login_input.setPlaceholderText('Login')
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setGeometry(QtCore.QRect(30, 140, 381, 31))
        self.password_input.setPlaceholderText('Password')
        self.password_input.setObjectName("default-input")

    def button(self):
        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.setGeometry(QtCore.QRect(140, 190, 151, 31))
        self.login_button.setObjectName('default-btn')
        self.login_button.setText('Login')
        self.login_button.clicked.connect(self.login)
        
    def title(self):
        self.login_title = QtWidgets.QLabel(self)
        self.login_title.setGeometry(QtCore.QRect(0, 0, 441, 71))
        self.login_title.setObjectName('login-title')
        self.login_title.setAlignment(QtCore.Qt.AlignCenter)
        self.login_title.setText('LOGIN')
    
    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()
        client = SteamClient(login, password)
        resp = client.login()
        if resp.get("requires_twofactor", False):
            self.code_window = CodeModalWindow(client, self, self.main_win)
            self.code_window.setupUi()
            self.code_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_form = LoginModalWindow()
    login_form.setupUi()
    login_form.show()
    sys.exit(app.exec_())