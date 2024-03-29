import json
import logging
import os
import webbrowser

from PyQt5 import QtCore, QtWidgets

from config import PATH_TO_TABLE_PAGE_STYLES, PATH_TO_LOG_PAGE_STYLES
from core.db.methods import (add_items, check_buy_items, check_sell_items,
                             delete_item, delete_items, get_item, get_items,
                             get_user, set_amount, set_amount_all,
                             set_buy_item, set_buy_items, set_buy_price,
                             set_buy_price_all, set_sell_item, set_sell_items,
                             set_sell_price, set_sell_price_all, 
                             get_items_count)
from core.db.models import Item
from core.utils import parse

from .components.buttons.GetJSONButton.GetJSONButton import GetJSONButton
from .modals import AddItemModalWindow, ProgressBarModalWindow
from .widgets import QTextEditLogger, ReadOnlyDelegate


class TablePage:
    def __init__(self, items, market):
        self.items = items
        self.market = market
        self.items_count = get_items_count()
        with open(PATH_TO_TABLE_PAGE_STYLES) as style:
            styles = style.read()
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("table_page")
        self.page.setStyleSheet(styles)
        self.title()
        self.table_widget()
        self.buttons_box()
        self.load_items()
        self.inputs()
        self.count_of_items()

    def inputs(self):
        self.search_input = QtWidgets.QLineEdit(self.page)
        self.search_input.setGeometry(QtCore.QRect(840, 15, 200, 31))
        self.search_input.setPlaceholderText("Search")
        self.search_input.setObjectName("default-input")
        self.search_input.textChanged.connect(self.search)

    def search(self):
        name = self.search_input.text().lower()
        for row in range(1, self.table.rowCount()):
            item = self.table.item(row, 0)
            self.table.setRowHidden(row, name not in item.text().lower())

    def title(self):
        self.title = QtWidgets.QLabel(self.page)
        self.title.setGeometry(QtCore.QRect(20, 10, 111, 41))
        self.title.setObjectName("title_table")
        self.title.setText("Table")

    def table_widget(self):
        self.table = QtWidgets.QTableWidget(self.page)
        self.table.setGeometry(QtCore.QRect(10, 60, 1071, 590))
        self.table.setObjectName("table")
        self.table.setColumnCount(7)
        self.table.setRowCount(0)
        for num in range(7):
            item = QtWidgets.QTableWidgetItem()
            self.table.setHorizontalHeaderItem(num, item)
        self.table.setHorizontalHeaderLabels(
            ["Item", "Amount", "Buy", "Sell", "Purchase", "Selling", "Action"]
        )
        
        self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 120)
        self.table.setColumnWidth(6, 113)
        delegate = ReadOnlyDelegate(self.table)
        self.table.setItemDelegateForColumn(0, delegate)
        self.table.verticalHeader().setVisible(False)

        self.no_items_label = QtWidgets.QLabel(self.page)
        self.no_items_label.setGeometry(QtCore.QRect(350, 60, 400, 590))
        self.no_items_label.setText("You don't have items in the database")
        self.no_items_label.setObjectName("no-items")
        self.no_items_label.hide()

        if not self.items:
            self.table.horizontalHeader().hide()
            self.no_items_label.show()
    
    def count_of_items(self):
        self.label_count_of_items = QtWidgets.QLabel(self.page)
        self.label_count_of_items.setText(f'Count of items: {self.items_count}')
        self.label_count_of_items.setGeometry(QtCore.QRect(680, 15, 150, 31))
        self.label_count_of_items.setObjectName("count-items")


    def set_item_value(self, item: QtWidgets.QTableWidgetItem):
        row, column = item.row(), item.column()
        text = self.table.horizontalHeaderItem(column).text().lower()
        to_change = f"{text}_all" if row == 0 else text

        item = self.table.item(row, 0).text()
        value = self.table.item(row, column).text()

        actions = {
            "amount": set_amount,
            "purchase": set_buy_price,
            "selling": set_sell_price,
            "amount_all": set_amount_all,
            "purchase_all": set_buy_price_all,
            "selling_all": set_sell_price_all,
        }

        if to_change in actions:
            actions[to_change](value) if row == 0 else actions[to_change](item, value)

        if row == 0:
            number_of_rows = self.table.rowCount()
            for r in range(1, number_of_rows):
                self.table.item(r, column).setText(value)

    def change_state(self, name: str, column: str):
        if column == "buy":
            set_buy_item(name)
            self.checkbox_buy_all.setChecked(check_buy_items())
        else:
            set_sell_item(name)
            self.checkbox_sell_all.setChecked(check_sell_items())

    def set_checkbox_state(self, item: Item):
        checkbox_buy = getattr(self, f"{item.name}_checkbox_buy")
        checkbox_sell = getattr(self, f"{item.name}_checkbox_sell")
        checkbox_buy.clicked.connect(lambda: self.change_state(item.name, "buy"))
        checkbox_buy.setChecked(item.buy_item)
        checkbox_sell.clicked.connect(lambda: self.change_state(item.name, "sell"))
        checkbox_sell.setChecked(item.sell_item)

    def load_items(self):
        row = 1
        if self.items:
            self.table.setRowCount(len(self.items) + 1)
            self.action_all()
            for item in self.items:
                self.add_item_to_table(item, row)
                row += 1
            self.table.horizontalHeader().show()
        self.table.itemChanged.connect(self.set_item_value)
        self.table.itemDoubleClicked.connect(self.open_url)

    def add_item_to_table(self, item: Item, row: int):
        widget_buy = QtWidgets.QWidget()
        widget_buy.setObjectName("checkbox")
        checkbox_buy = QtWidgets.QCheckBox()
        setattr(self, f"{item.name}_checkbox_buy", checkbox_buy)

        layout_buy = QtWidgets.QHBoxLayout(widget_buy)
        layout_buy.addWidget(checkbox_buy)
        layout_buy.setAlignment(QtCore.Qt.AlignCenter)

        widget_sell = QtWidgets.QWidget()
        widget_sell.setObjectName("checkbox")
        checkbox_sell = QtWidgets.QCheckBox()
        setattr(self, f"{item.name}_checkbox_sell", checkbox_sell)

        self.set_checkbox_state(item)

        layout_sell = QtWidgets.QHBoxLayout(widget_sell)
        layout_sell.addWidget(checkbox_sell)
        layout_sell.setAlignment(QtCore.Qt.AlignCenter)

        button_delete = QtWidgets.QPushButton()
        button_delete.setText("Delete")
        button_delete.setObjectName("delete-btn")
        button_delete.clicked.connect(lambda: self.delete_item(item.name))

        item_name = QtWidgets.QTableWidgetItem(item.name)

        amount = QtWidgets.QTableWidgetItem(str(item.amount))
        amount.setTextAlignment(QtCore.Qt.AlignCenter)

        purschase = QtWidgets.QTableWidgetItem(str(item.buy_price))
        purschase.setTextAlignment(QtCore.Qt.AlignCenter)

        selling = QtWidgets.QTableWidgetItem(str(item.sell_price))
        selling.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setItem(row, 0, item_name)
        self.table.setItem(row, 1, amount)
        self.table.setCellWidget(row, 2, widget_buy)
        self.table.setCellWidget(row, 3, widget_sell)
        self.table.setItem(row, 4, purschase)
        self.table.setItem(row, 5, selling)
        self.table.setCellWidget(row, 6, button_delete)

    def open_url(self, item: QtWidgets.QTableWidgetItem):
        if item.column() == 0 and item.row() > 0:
            item = get_item(item.text())
            webbrowser.open(item.steam_url)

    def change_all_states(self, state: bool, column: str):
        set_buy_items(state) if column == "buy" else set_sell_items(state)
        items = get_items()

        for item in items:
            checkbox = getattr(self, f"{item.name}_checkbox_{column}")
            checkbox.setChecked(item.buy_item if column == "buy" else item.sell_item)

    def delete_item(self, name: str):
        row = self.table.currentRow()
        delete_item(name)
        self.table.removeRow(row)
        self.items_count -= 1
        
        if not get_items():
            self.table.setRowCount(0)
            self.table.horizontalHeader().hide()
            self.no_items_label.show()
            self.items_count = 0
        self.label_count_of_items.setText(f'Count of items: {self.items_count}')

    def delete_items(self):
        delete_items()
        self.table.setRowCount(0)
        self.table.horizontalHeader().hide()
        self.no_items_label.show()

        self.items_count = 0
        self.label_count_of_items.setText(f'Count of items: {self.items_count}')

    def action_all(self):
        widget_buy = QtWidgets.QWidget()
        widget_buy.setObjectName("checkbox")

        self.checkbox_buy_all = QtWidgets.QCheckBox()
        self.checkbox_buy_all.clicked.connect(
            lambda: self.change_all_states(self.checkbox_buy_all.isChecked(), "buy")
        )
        self.checkbox_buy_all.setChecked(check_buy_items())

        layout_buy = QtWidgets.QHBoxLayout(widget_buy)
        layout_buy.addWidget(self.checkbox_buy_all)
        layout_buy.setAlignment(QtCore.Qt.AlignCenter)

        widget_sell = QtWidgets.QWidget()
        widget_sell.setObjectName("checkbox")

        self.checkbox_sell_all = QtWidgets.QCheckBox()
        self.checkbox_sell_all.clicked.connect(
            lambda: self.change_all_states(self.checkbox_sell_all.isChecked(), "sell")
        )
        self.checkbox_sell_all.setChecked(check_sell_items())

        layout_sell = QtWidgets.QHBoxLayout(widget_sell)
        layout_sell.addWidget(self.checkbox_sell_all)
        layout_sell.setAlignment(QtCore.Qt.AlignCenter)

        button_delete = QtWidgets.QPushButton()
        button_delete.setText("Delete")
        button_delete.setObjectName("delete-btn")
        button_delete.clicked.connect(lambda: self.delete_items())

        amount = QtWidgets.QTableWidgetItem("0")
        amount.setTextAlignment(QtCore.Qt.AlignCenter)

        purschase = QtWidgets.QTableWidgetItem("0.0")
        purschase.setTextAlignment(QtCore.Qt.AlignCenter)

        selling = QtWidgets.QTableWidgetItem("0.0")
        selling.setTextAlignment(QtCore.Qt.AlignCenter)

        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem("*"))
        self.table.setItem(0, 1, amount)
        self.table.setCellWidget(0, 2, widget_buy)
        self.table.setCellWidget(0, 3, widget_sell)
        self.table.setItem(0, 4, purschase)
        self.table.setItem(0, 5, selling)
        self.table.setCellWidget(0, 6, button_delete)

    def buttons_box(self):
        self.buttons_area_right = QtWidgets.QWidget(self.page)
        self.buttons_area_right.setGeometry(QtCore.QRect(810, 650, 271, 80))
        self.buttons_area_right.setObjectName("buttons_area_table")
        self.buttons_layout_right = QtWidgets.QHBoxLayout(self.buttons_area_right)
        self.buttons_layout_right.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout_right.setSpacing(6)
        self.buttons_layout_right.setObjectName("buttons_layout")

        self.buttons_area_left = QtWidgets.QWidget(self.page)
        self.buttons_area_left.setGeometry(QtCore.QRect(20, 650, 271, 80))
        self.buttons_area_left.setObjectName("buttons_area_table")
        self.buttons_layout_left = QtWidgets.QHBoxLayout(self.buttons_area_left)
        self.buttons_layout_left.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout_left.setSpacing(6)
        self.buttons_layout_left.setObjectName("buttons_layout")

        self.buttons()

    def buttons(self):
        self.add_item_btn = QtWidgets.QPushButton(self.buttons_area_right)
        self.add_item_btn.setObjectName("default-btn")
        self.add_item_btn.setText("Add Item")
        self.add_item_btn.clicked.connect(self.open_add_item_window)
        self.buttons_layout_right.addWidget(self.add_item_btn)

        self.update_table_btn = QtWidgets.QPushButton(self.buttons_area_right)
        self.update_table_btn.setObjectName("default-btn")
        self.update_table_btn.setText("Update Table")
        self.update_table_btn.clicked.connect(self.update_table)
        self.buttons_layout_right.addWidget(self.update_table_btn)

        self.remove_orders_btn = QtWidgets.QPushButton(self.buttons_area_left)
        self.remove_orders_btn.setObjectName("default-btn")
        self.remove_orders_btn.setText("Remove orders")
        self.remove_orders_btn.clicked.connect(
            lambda: self.open_progress_bar_window("orders")
        )
        self.buttons_layout_left.addWidget(self.remove_orders_btn)

        self.remove_unprofitable_btn = QtWidgets.QPushButton(self.buttons_area_left)
        self.remove_unprofitable_btn.setObjectName("default-btn")
        self.remove_unprofitable_btn.setText("Remove bad items")
        self.remove_unprofitable_btn.clicked.connect(
            lambda: self.open_progress_bar_window("unprofitable")
        )
        self.buttons_layout_left.addWidget(self.remove_unprofitable_btn)

        self.upload_table_btn = GetJSONButton(self.page)
        self.upload_table_btn.setGeometry(QtCore.QRect(1051, 15, 30, 30))
        self.upload_table_btn.clicked.connect(self.upload_table)

    def upload_table(self):
        dlg = QtWidgets.QFileDialog()
        directory = dlg.getExistingDirectory(self.page, "Select folder")

        if directory != "":
            items = get_items()
            user = get_user()
            data = []

            for item in items:
                name, game_id = parse(item.steam_url)
                data.append({"name": name, "game": game_id, "url": item.steam_url})

            with open(f"{directory}/{user.account_name}_items.json", "w") as f:
                f.write(json.dumps(data, indent=4))

    def update_table(self):
        dlg = QtWidgets.QFileDialog()
        path_to_json_file = dlg.getOpenFileName(
            self.page, "Select file", os.getcwd(), "JSON document (*.json)"
        )[0]

        if path_to_json_file != "" and self.validate_items_file(path_to_json_file):
            delete_items()
            self.table.setRowCount(1)
            add_items(path_to_json_file)
            items = get_items()
            
            self.table.horizontalHeader().show()
            self.no_items_label.hide()
            self.action_all()

            for item in items:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.add_item_to_table(item, row)
            
            self.items_count = get_items_count()
            self.label_count_of_items.setText(f'Count of items: {self.items_count}')

    def validate_items_file(self, path: str):
        with open(path) as items_json:
            items = json.load(items_json)

        for item in items:
            if len(item) != 3 or list(item.keys()) != ["name", "game", "url"]:
                return False

        return True

    def open_add_item_window(self):
        self.window_add_item = AddItemModalWindow(self)
        self.window_add_item.setupUi()
        self.window_add_item.show()

    def open_progress_bar_window(self, action: str):
        self.window_progress_bar = ProgressBarModalWindow(self.market, action, self)
        self.window_progress_bar.setupUi()
        self.window_progress_bar.setWindowModality(QtCore.Qt.ApplicationModal)
        self.window_progress_bar.show()


class LogPage:
    def __init__(self) -> None:
        with open(PATH_TO_LOG_PAGE_STYLES) as style:
            styles = style.read()
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("log_page")
        self.page.setStyleSheet(styles)
        self.title()
        self.log_area()
        self.buttons()

    def title(self):
        self.title = QtWidgets.QLabel(self.page)
        self.title.setGeometry(QtCore.QRect(20, 10, 111, 41))
        self.title.setObjectName("title_log")
        self.title.setText("Logs")

    def buttons(self):
        self.clear_btn = QtWidgets.QPushButton(self.page)
        self.clear_btn.setGeometry(QtCore.QRect(10, 675, 1071, 30))
        self.clear_btn.setText("Clear")
        self.clear_btn.setObjectName("clear-btn")
        self.clear_btn.clicked.connect(self.log_box.log_widget.clear)

    def log_area(self):
        self.log_box = QTextEditLogger(self.page)
        self.log_box.setFormatter(
            logging.Formatter("%(asctime)s - %(message)s", "%H:%M:%S")
        )
        self.log_box.log_widget.setGeometry(QtCore.QRect(10, 60, 1071, 600))
        logging.getLogger().addHandler(self.log_box)
        logging.getLogger().setLevel(logging.INFO)
