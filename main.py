import sys

from PyQt5 import QtWidgets, QtCore

from ui.widgets import Sidebar
from ui.pages import TablePage, LogPage, SettingPage
from ui.modals import LoginModalWindow

from core.db.methods import is_user_login, get_user, get_items
from core.login import do_login

from core.utils import get_secrets
from steamlib.guard import SteamGuard


class MainWindow(QtWidgets.QMainWindow):
    def setupUi(self):
        with open('steam-trade/ui/css/main.css') as style:
            styles = style.read()
        self.user = get_user()
        self.items = get_items()
        self.session = do_login()
        self.guard = SteamGuard(self.session, get_secrets(self.user))
        self.setObjectName('MainWindow')
        self.resize(1280, 720)
        self.sidebar = Sidebar(self, self.user, self.session, self.guard)
        self.main = QtWidgets.QStackedWidget(self)
        self.main.setGeometry(QtCore.QRect(180, 0, 1121, 720))
        self.main.setObjectName("main")
        self.table = TablePage(self.items)
        self.logs = LogPage()
        self.settings = SettingPage()
        self.main.addWidget(self.table.page)
        self.main.setCurrentWidget(self.table.page)
        self.main.addWidget(self.logs.page)
        self.main.addWidget(self.settings.page)
        self.page_buttons()
        self.main.setStyleSheet(styles)
    
    def page_buttons(self):
        self.sidebar.table_button.clicked.connect(lambda: self.set_current_page(self.table.page, self.sidebar.table_button))
        self.sidebar.log_button.clicked.connect(lambda: self.set_current_page(self.logs.page, self.sidebar.log_button))
        self.sidebar.settings_button.clicked.connect(lambda: self.set_current_page(self.settings.page, self.sidebar.settings_button))
    
    def set_current_page(self, page, button):
        buttons = [self.sidebar.log_button, self.sidebar.table_button, self.sidebar.settings_button]
        self.main.setCurrentWidget(page)
        button.setStyleSheet('background-color: #1b1c22;')
        for btn in buttons:
            if btn != button:
                btn.setStyleSheet('QPushButton {color: #acacae; font-size: 14px; border: none; background-color: #25262c} QPushButton::hover {background-color: #1b1c22;}')

    def restart(self):
        QtCore.QCoreApplication.quit()
        QtCore.QProcess.startDetached(sys.executable, sys.argv)
    
    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    login = is_user_login()
    if not login:
        login_win = LoginModalWindow(win)
        login_win.setupUi()
        login_win.show()
    else:
        win.setupUi()
        win.show()
    sys.exit(app.exec_())
    