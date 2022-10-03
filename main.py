import sys

from PyQt5 import QtCore, QtWidgets

from core.db.methods import (create_db, get_items, get_secrets, get_user,
                             is_user_login)
from core.login import do_login
from core.market import Market
from steamlib.guard import SteamGuard
from ui.modals import LoginModalWindow
from ui.pages import LogPage, TablePage
from ui.widgets import Sidebar


class MainWindow(QtWidgets.QMainWindow):
    def setupUi(self):
        with open("steam-trade/ui/styles/main.qss") as style:
            styles = style.read()
        self.user = get_user()
        self.setWindowTitle('Steam Arbitrage')
        self.items = get_items()
        self.session = do_login()
        self.secrets = get_secrets()
        self.guard = SteamGuard(self.session, self.secrets)
        self.market = Market(self.session, self.secrets)
        self.setObjectName("MainWindow")
        self.setFixedSize(1280, 720)
        self.center()
        self.sidebar = Sidebar(self, self.user, self.session, self.guard, self.secrets)
        self.main = QtWidgets.QStackedWidget(self)
        self.main.setGeometry(QtCore.QRect(180, 0, 1121, 720))
        self.main.setObjectName("main")
        self.table = TablePage(self.items, self.market)
        self.logs = LogPage()
        self.main.addWidget(self.table.page)
        self.main.setCurrentWidget(self.table.page)
        self.main.addWidget(self.logs.page)
        self.page_buttons()
        self.main.setStyleSheet(styles)

    def page_buttons(self):
        self.sidebar.table_button.clicked.connect(
            lambda: self.set_current_page(self.table.page, self.sidebar.table_button)
        )
        self.sidebar.log_button.clicked.connect(
            lambda: self.set_current_page(self.logs.page, self.sidebar.log_button)
        )

    def set_current_page(self, page, button):
        buttons = [self.sidebar.log_button, self.sidebar.table_button]
        self.main.setCurrentWidget(page)
        button.setStyleSheet("background-color: #1b1c22;")
        for btn in buttons:
            if btn != button:
                btn.setStyleSheet(
                    "QPushButton {color: #acacae; font-size: 14px; border: none; background-color: #25262c} QPushButton::hover {background-color: #1b1c22;}"
                )

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def restart(self):
        QtCore.QCoreApplication.quit()
        QtCore.QProcess.startDetached(sys.executable, sys.argv)

    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    create_db()
    main_win = MainWindow()
    login = is_user_login()
    if not login:
        login_win = LoginModalWindow(main_win)
        login_win.setupUi()
        login_win.show()
    else:
        main_win.setupUi()
        main_win.show()
    sys.exit(app.exec_())
