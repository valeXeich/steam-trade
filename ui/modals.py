import time
import sip

from PyQt5 import QtCore, QtWidgets, QtGui

from steamlib.client import SteamClient
from steamlib.exceptions import InvalidDataError
from steamlib.models import APIEndpoint
from core.db.methods import add_user, add_item, get_users, delete_user, change_user, get_last_added_user
import requests


class AddItemModalWindow(QtWidgets.QMainWindow):
    def __init__(self, table_page):
        super().__init__()
        self.table_page = table_page
    
    def setupUi(self):
        with open('steam-trade/ui/css/modals.css') as style:
            styles = style.read()
        self.setObjectName('AddItemModal')
        self.setWindowTitle('Add Item')
        self.setStyleSheet(styles)
        self.setFixedSize(488, 121)
        self.button()
        self.inputs()
        self.error_message()
        self.center()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def button(self):
        self.btn_add = QtWidgets.QPushButton(self)
        self.btn_add.setGeometry(QtCore.QRect(150, 70, 181, 31))
        self.btn_add.setObjectName("default-btn")
        self.btn_add.setText('Add Item')
        self.btn_add.clicked.connect(self.add_item_to_db)
    
    def inputs(self):
        self.item_input = QtWidgets.QLineEdit(self)
        self.item_input.setGeometry(QtCore.QRect(20, 20, 451, 31))
        self.item_input.setPlaceholderText('URL')
        self.item_input.setObjectName("default-input")

    def error_message(self):
        self.url_error_message = QtWidgets.QLabel(self)
        self.url_error_message.setGeometry(QtCore.QRect(20, 115, 451, 31))
        self.url_error_message.setObjectName('error-message')
        self.url_error_message.setWordWrap(True)
    
    def add_item_to_db(self):
        item = self.validate_url()
        
        if not isinstance(item, bool):
            row = self.table_page.table.rowCount()
            self.table_page.table.insertRow(row)
            self.table_page.add_item_to_table(item, row)
            time.sleep(.3)
            self.close()
    
    def validate_url(self):
        try:
            item = add_item(self.item_input.text())
        except (KeyError, IndexError):
            self.item_input.clear()
            self.setFixedSize(488, 160)
            self.url_error_message.setText("Bad url (Invalid item url or game doesn't exist in the database or this item already in the database).")
            return False
        return item


class CodeModalWindow(QtWidgets.QMainWindow):
    def __init__(self, client, login_modal_window, main_window=None, is_email_need=False):
        super().__init__()
        self.client = client
        self.login_modal_window = login_modal_window
        self.main_window = main_window
        self.email = is_email_need
    
    def setupUi(self):
        with open('steam-trade/ui/css/modals.css') as style:
            styles = style.read()
        self.setObjectName('Code')
        self.setWindowTitle('Code')
        self.setStyleSheet(styles)
        self.setFixedSize(223, 152)
        self.title()
        self.inputs()
        self.button()
        self.error_message()
        self.center()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def title(self):
        self.code_title = QtWidgets.QLabel(self)
        self.code_title.setGeometry(QtCore.QRect(-10, 0, 251, 31))
        self.code_title.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.code_title.setObjectName('code-title')
        self.code_title.setText('Enter your code')
        
    def inputs(self):
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
        
    def error_message(self):
        self.invalid_code_message = QtWidgets.QLabel(self)
        self.invalid_code_message.setGeometry(QtCore.QRect(10, 140, 201, 31))
        self.invalid_code_message.setObjectName('error-message')
        
    def send_code(self, session, need_code=True):
        resp = self.get_response(session, need_code)
        
        if isinstance(resp, dict) and not resp['success']:
            self.setFixedSize(223, 180)
            self.invalid_code_message.setText('Invalid code.')
        else:
            cookies = resp.cookies.get_dict()
            if cookies.get('sessionid', False):
                add_user(self.client.username, self.client._session)
                self.close()
                time.sleep(.5)
                self.login_modal_window.close()
                time.sleep(.5)
                self.main_window.setupUi()
                self.main_window.show()

    def get_response(self, session, need_code):
        if need_code:
            if self.email:
                response = self.client.login(email_code=self.code_input.text())
            else:
                response = self.client.login(twofactor_code=self.code_input.text())
        else:
            response = session
        return response


class SelectAccountCodeModalWindow(CodeModalWindow):
    def __init__(self, client, login_modal_window, account_modal, is_email_need=False):
        super().__init__(client, login_modal_window, is_email_need)
        self.account_modal = account_modal
        self.email = is_email_need
    
    def send_code(self, session, need_code=True):
        resp = self.get_response(session, need_code)
            
        if isinstance(resp, dict) and not resp['success']:
            self.setFixedSize(223, 180)
            self.invalid_code_message.setText('Invalid code.')
        else:
            cookies = resp.cookies.get_dict()
            if cookies.get('sessionid', False):
                add_user(self.client.username, self.client._session, False)
                self.close()
                time.sleep(.5)
                self.login_modal_window.close()
                user = get_last_added_user()
                self.account_modal.create_frame(user)
                self.account_modal.set_geometry()


class LoginModalWindow(QtWidgets.QMainWindow):
    def __init__(self, main_win=None, account_select=False, account_modal=None):
        super().__init__()
        self.main_win = main_win
        self.account_select = account_select
        self.account_modal = account_modal
        self.captcha_data = {'captcha_gid': '', 'captcha_text': ''}
    
    def setupUi(self):
        with open('steam-trade/ui/css/modals.css') as style:
            styles = style.read()
        self.setObjectName('Login')
        self.setFixedSize(441, 250)
        self.policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.policy.setHorizontalStretch(0)
        self.policy.setVerticalStretch(0)
        self.policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(self.policy)
        self.setWindowTitle('Login')
        self.setStyleSheet(styles)
        self.center()
        self.title()
        self.inputs()
        self.button()
        self.error_messages()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
        
        self.captcha_input = QtWidgets.QLineEdit(self)
        self.captcha_input.setGeometry(QtCore.QRect(30, 330, 381, 31))
        self.captcha_input.setObjectName("default-input")
        self.captcha_input.setPlaceholderText('Captcha')

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
    
    def error_messages(self):
        self.login_error_message = QtWidgets.QLabel(self)
        self.login_error_message.setGeometry(QtCore.QRect(30, 240, 381, 35))
        self.login_error_message.setWordWrap(True)
        self.login_error_message.setObjectName('error-message')
        
        self.captcha_image = QtWidgets.QLabel(self)
        self.captcha_image.setGeometry(QtCore.QRect(30, 280, 206, 40))
        self.captcha_image.setScaledContents(True)
    
    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()
        client = SteamClient(login, password)
        self.captcha_data['captcha_text'] = self.captcha_input.text()
        self.captcha_input.clear()
        
        try:
            resp = client.login(captcha=self.captcha_data)
        except InvalidDataError:
            resp = {'message': "The account name or password that you have entered is incorrect."}
        
        if isinstance(resp, requests.Session):
            if self.account_select:
                SelectAccountCodeModalWindow(client, self, self.account_modal).send_code(resp, need_code=False)
            else:
                CodeModalWindow(client, self, self.main_win).send_code(resp, need_code=False)
            return
                
        if "account name or password" in resp.get("message", ""):
            self.login_error_message.setText(resp.get("message", ""))
            self.setFixedSize(441, 300)
            self.password_input.clear()
            self.captcha_input.deleteLater()
            self.captcha_image.clear()
            
        if "too many login failures" in resp.get("message", ""):
            self.password_input.clear()
            self.login_error_message.setText(resp.get("message", ""))
            self.setFixedSize(441, 300) 
            self.captcha_input.deleteLater()
            self.captcha_image.clear()
            
        if resp.get("captcha_needed", False) and 'too many login failures' not in resp.get("message", ""):
            self.password_input.clear()
            self.login_error_message.setText(resp.get("message", ""))
            self.setFixedSize(441, 370)
            self.captcha = QtGui.QImage()
            captcha_gid = resp.get("captcha_gid")
            self.captcha.loadFromData(requests.get(f'{APIEndpoint.COMMUNITY_URL}login/rendercaptcha/?gid={captcha_gid}').content) 
            self.captcha_image.setPixmap(QtGui.QPixmap(self.captcha))
            self.captcha_data['captcha_gid'] = captcha_gid
        
        if resp.get("requires_twofactor", False) or resp.get("emailauth_needed", False):
            email = resp.get("emailauth_needed", False)
            if self.account_select:
                self.code_window = SelectAccountCodeModalWindow(client, self, self.account_modal, is_email_need=email)
            else:
                self.code_window = CodeModalWindow(client, self, self.main_win, is_email_need=email)
            self.code_window.setupUi()
            self.code_window.show()


class AccountSelectModalWindow(QtWidgets.QMainWindow):
    def __init__(self, restart):
        super().__init__()
        self.data = {
            'one': {
                'size': [564, 230],
                'scroll': [20, 70, 531, 101],
                'scroll_widget': [0, 0, 529, 99],
                'button': [230, 190, 89, 25]
            },
            'many': {
                'size': [564, 310],
                'scroll': [20, 70, 531, 181],
                'scroll_widget': [0, 0, 529, 179],
                'button': [250, 270, 89, 25]
            }
        }
        self.accounts = get_users()
        self.restart = restart

    def setupUi(self):
        self.setObjectName('AccountSelect')
        self.setStyleSheet("background-color: #1b1c22;")
        self.title()
        self.scroll()
        self.button()
        self.set_geometry()
        self.center()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def set_geometry(self):
        self.accounts = get_users()
        self.params = self.data['one'] if len(get_users()) == 1 else self.data['many']
        self.setFixedSize(*self.params['size'])
        self.account_scrollArea.setGeometry(QtCore.QRect(*self.params['scroll']))
        self.account_scrollAreaWidgetContents.setGeometry(QtCore.QRect(*self.params['scroll_widget']))
        self.add_account_btn.setGeometry(QtCore.QRect(*self.params['button']))

    def title(self):
        self.account_title = QtWidgets.QLabel(self)
        self.account_title.setGeometry(QtCore.QRect(9, 9, 551, 51))
        self.account_title.setStyleSheet("color: #acacae; font-weight: bold; font-size: 24px;")
        self.account_title.setAlignment(QtCore.Qt.AlignCenter)
        self.account_title.setObjectName("account-title")
        self.account_title.setText('Choose account')

    def scroll(self):
        self.account_scrollArea = QtWidgets.QScrollArea(self)
        #self.account_scrollArea.setGeometry(QtCore.QRect(*self.params['scroll']))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_scrollArea.sizePolicy().hasHeightForWidth())
        self.account_scrollArea.setSizePolicy(sizePolicy)
        self.account_scrollArea.setWidgetResizable(True)
        self.account_scrollArea.setObjectName("account-scrollArea")
        self.account_scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.account_scrollAreaWidgetContents.setGeometry(QtCore.QRect(*self.params['scroll_widget']))
        self.account_scrollAreaWidgetContents.setObjectName("account-scrollAreaWidgetContents")
        self.account_scrollArea.setStyleSheet('QScrollArea {border: none;}')
        self.frame()
        self.account_scrollArea.setWidget(self.account_scrollAreaWidgetContents)
    
    def frame(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self.account_scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        for account in self.accounts:
            self.create_frame(account)
    
    def create_frame(self, account):
        self.account_box = QtWidgets.QFrame(self.account_scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.account_box.sizePolicy().hasHeightForWidth())
        self.account_box.setSizePolicy(sizePolicy)
        self.account_box.setMinimumSize(QtCore.QSize(0, 70))
        self.account_box.setMaximumSize(QtCore.QSize(16777215, 70))
        self.account_box.setStyleSheet("background-color: #2f3136; border-radius: 5px;")
        self.account_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.account_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.account_box.setObjectName("account-box")
        self.get_avatar(account)
        self.get_username(account)
        if account.is_login:
            self.is_active()
        self.action_buttons(self.account_box, account)
        self.verticalLayout.addWidget(self.account_box)
    
    def get_avatar(self, user):
        self.avatar = QtGui.QImage()
        self.avatar.loadFromData(requests.get(user.avatar).content)
        self.avatar_lbl = QtWidgets.QLabel(self.account_box)
        self.avatar_lbl.setGeometry(QtCore.QRect(9, 10, 50, 51))   
        self.avatar_lbl.setPixmap(QtGui.QPixmap(self.avatar))
        self.avatar_lbl.setScaledContents(True)

    def get_username(self, user):
        self.username = QtWidgets.QLabel(self.account_box)
        self.username.setGeometry(QtCore.QRect(65, -5, 250, 51))
        self.username.setObjectName("username")
        self.username.setStyleSheet('color: #fff; font-size: 14px;')
        self.username.setText(user.account_name)
    
    def is_active(self):
        self.active = QtWidgets.QLabel(self.account_box)
        self.active.setGeometry(QtCore.QRect(65, 40, 67, 17))
        self.active.setObjectName("active")
        self.active.setText('Active')
        self.active.setStyleSheet('color: #3ba55d; font-weight: bold; font-size: 14px;')
    
    def button(self):
        self.add_account_btn = QtWidgets.QPushButton(self)
        # self.add_account.setGeometry(QtCore.QRect(*self.params['button']))
        self.add_account_btn.setObjectName("add-account-btn")
        self.add_account_btn.setText('Add account')
        self.add_account_btn.clicked.connect(self.add_account)
    
    def action_buttons(self, frame, account):
        self.delete_btn = QtWidgets.QPushButton(frame)
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.setGeometry(QtCore.QRect(470, 30, 15, 15))
        self.delete_btn.setStyleSheet('QPushButton {background-color: #ad473f; border-radius: 7px;} QPushButton::hover {background-color: #8d362f}')
        self.delete_btn.clicked.connect(lambda: self.delete_account(frame, account))

        if not account.is_login:
            self.switch_btn = QtWidgets.QPushButton(frame)
            self.switch_btn.setObjectName("delete_btn")
            self.switch_btn.setGeometry(QtCore.QRect(440, 30, 15, 15))
            self.switch_btn.setStyleSheet('QPushButton {background-color: #3c50fa; border-radius: 7px;} QPushButton::hover {background-color: #2834a3}')
            self.switch_btn.clicked.connect(lambda: self.switch_account(account))
    
    def delete_account(self, frame, account):
        delete_user(account)
        if account.is_login:
            self.restart()
        self.verticalLayout.removeWidget(frame)
        sip.delete(frame)
        self.set_geometry()
    
    def switch_account(self, account):
        change_user(account)
        self.restart()

    def add_account(self):
        self.login_window = LoginModalWindow(account_select=True, account_modal=self)
        self.login_window.setupUi()
        self.login_window.show()
