import logging

from PyQt5 import QtWidgets, QtCore

from .widgets import QTextEditLogger
from .modals import AddItemModalWindow

class TablePage:
    def __init__(self) -> None:
        with open('steam-trade/ui/css/table-page.css') as style:
            styles = style.read()
        self.page = QtWidgets.QWidget()
        self.page.setObjectName('table_page')
        self.page.setStyleSheet(styles)
        self.title()
        self.table()
        self.buttons_box()

    def title(self):
        self.title = QtWidgets.QLabel(self.page)
        self.title.setGeometry(QtCore.QRect(20, 10, 111, 41))
        self.title.setObjectName("title_table")
        self.title.setText('Table')

    def table(self):
        self.table = QtWidgets.QTableWidget(self.page)
        self.table.setGeometry(QtCore.QRect(10, 60, 1071, 590))
        self.table.setObjectName('table')
        self.table.setColumnCount(7)
        self.table.setRowCount(0)
        for num in range(7):
            item = QtWidgets.QTableWidgetItem()
            self.table.setHorizontalHeaderItem(num, item)
        self.table.setHorizontalHeaderLabels(['Item', 'Amount', 'Buy', 'Sell', 'Purchase', 'Selling', 'Action'])
        self.table.setColumnWidth(0, 438)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 120)
    
    def buttons_box(self):
        self.buttons_area = QtWidgets.QWidget(self.page)
        self.buttons_area.setGeometry(QtCore.QRect(810, 650, 271, 80))
        self.buttons_area.setObjectName('buttons_area_table')
        self.buttons_layout = QtWidgets.QHBoxLayout(self.buttons_area)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(6)
        self.buttons_layout.setObjectName("buttons_layout")
        self.buttons()
    
    def buttons(self):
        self.add_item_btn = QtWidgets.QPushButton(self.buttons_area)
        self.add_item_btn.setObjectName('default-btn')
        self.add_item_btn.setText('Add Item')
        self.add_item_btn.clicked.connect(self.open_add_item)
        self.buttons_layout.addWidget(self.add_item_btn)
        self.update_table_btn = QtWidgets.QPushButton(self.buttons_area)
        self.update_table_btn.setObjectName('default-btn')
        self.update_table_btn.setText('Update Table')
        self.buttons_layout.addWidget(self.update_table_btn)
    
    def open_add_item(self):
        self.window_add_item = AddItemModalWindow()
        self.window_add_item.setupUi()
        self.window_add_item.show()


class LogPage:
    def __init__(self) -> None:
        with open('steam-trade/ui/css/log-page.css') as style:
            styles = style.read()
        self.page = QtWidgets.QWidget()
        self.page.setObjectName('log_page')
        self.page.setStyleSheet(styles)
        self.title()
        self.log_area()

    def title(self):
        self.title = QtWidgets.QLabel(self.page)
        self.title.setGeometry(QtCore.QRect(20, 10, 111, 41))
        self.title.setObjectName("title_log")
        self.title.setText('Logs')

    def log_area(self):
        self.log_box = QTextEditLogger(self.page)
        self.log_box.setFormatter(logging.Formatter('%(asctime)s - %(message)s', "%H:%M:%S"))
        self.log_box.widget.setGeometry(QtCore.QRect(10, 60, 1071, 631))
        logging.getLogger().addHandler(self.log_box)
        logging.getLogger().setLevel(logging.DEBUG)


class SettingPage:
    def __init__(self) -> None:
        with open('steam-trade/ui/css/settings-page.css') as style:
            styles = style.read()
        self.page = QtWidgets.QWidget()
        self.page.setObjectName('setting_page')
        self.page.setStyleSheet(styles)
        self.title()
    
    def title(self):
        self.title = QtWidgets.QLabel(self.page)
        self.title.setGeometry(QtCore.QRect(20, 10, 111, 41))
        self.title.setObjectName("title_setting")
        self.title.setText('Settings')