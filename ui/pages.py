import logging
import webbrowser
import os
import json

from PyQt5 import QtWidgets, QtCore

from .widgets import QTextEditLogger, ReadOnlyDelegate
from .modals import AddItemModalWindow
from core.db.methods import ( 
    add_items,
    get_item,
    get_items,
    delete_item, 
    delete_items,
    set_buy_item, 
    set_buy_items,
    check_buy_items,
    set_sell_item,
    set_sell_items,
    check_sell_items,
    set_amount,
    set_amount_all,
    set_buy_price,
    set_buy_price_all,
    set_sell_price,
    set_sell_price_all,  
)

class TablePage:
    def __init__(self, items):
        self.items = items
        with open('steam-trade/ui/css/table-page.css') as style:
            styles = style.read()
        self.page = QtWidgets.QWidget()
        self.page.setObjectName('table_page')
        self.page.setStyleSheet(styles)
        self.title()
        self.table_widget()
        self.buttons_box()
        self.load_items()

    def title(self):
        self.title = QtWidgets.QLabel(self.page)
        self.title.setGeometry(QtCore.QRect(20, 10, 111, 41))
        self.title.setObjectName("title_table")
        self.title.setText('Table')

    def table_widget(self):
        self.table = QtWidgets.QTableWidget(self.page)
        self.table.setGeometry(QtCore.QRect(10, 60, 1071, 590))
        self.table.setObjectName('table')
        self.table.setColumnCount(7)
        self.table.setRowCount(0)
        for num in range(7):
            item = QtWidgets.QTableWidgetItem()
            self.table.setHorizontalHeaderItem(num, item)
        self.table.setHorizontalHeaderLabels(['Item', 'Amount', 'Buy', 'Sell', 'Purchase', 'Selling', 'Action'])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table.setColumnWidth(0, 438)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 120)
        self.table.setColumnWidth(6, 113)
        delegate = ReadOnlyDelegate(self.table)
        self.table.setItemDelegateForColumn(0, delegate)
          
    def set_item_value(self, item):
        row, column = item.row(), item.column()
        text = self.table.horizontalHeaderItem(column).text().lower()
        to_change = f'{text}_all' if row == 0 else text
        
        item = self.table.item(row, 0).text()
        value = self.table.item(row, column).text()
        
        actions = {
            'amount': set_amount,
            'purchase': set_buy_price,
            'selling': set_sell_price,
            'amount_all': set_amount_all,
            'purchase_all': set_buy_price_all,
            'selling_all': set_sell_price_all
        } 
        
        if to_change in actions:
            actions[to_change](value) if row == 0 else actions[to_change](item, value)
        
        if row == 0:
            number_of_rows = self.table.rowCount()
            for r in range(1, number_of_rows):
                self.table.item(r, column).setText(value)
            
    def change_state(self, name, column):
        if column == 'buy':
           set_buy_item(name) 
           self.checkbox_buy_all.setChecked(check_buy_items()) 
        else:
            set_sell_item(name)
            self.checkbox_sell_all.setChecked(check_sell_items())     
        
        
    def set_checkbox_state(self, item):
        checkbox_buy = getattr(self, f'{item.name}_checkbox_buy')
        checkbox_sell = getattr(self, f'{item.name}_checkbox_sell')
        checkbox_buy.clicked.connect(lambda: self.change_state(item.name, 'buy'))
        checkbox_buy.setChecked(item.buy_item)
        checkbox_sell.clicked.connect(lambda: self.change_state(item.name, 'sell'))
        checkbox_sell.setChecked(item.sell_item)
    
    def load_items(self):
        row = 1
        self.table.setRowCount(len(self.items) + 1)
        self.action_all()
        self.table.verticalHeader().setVisible(False)
        for item in self.items:
            self.add_item_to_table(item, row)
            row += 1
            
        self.table.itemChanged.connect(self.set_item_value)
        self.table.itemDoubleClicked.connect(self.open_url)
    
    def add_item_to_table(self, item, row):
        widget_buy = QtWidgets.QWidget()
        widget_buy.setObjectName('checkbox')
        checkbox_buy = QtWidgets.QCheckBox()
        setattr(self, f'{item.name}_checkbox_buy', checkbox_buy)
        
        layout_buy = QtWidgets.QHBoxLayout(widget_buy)
        layout_buy.addWidget(checkbox_buy)
        layout_buy.setAlignment(QtCore.Qt.AlignCenter)

        widget_sell = QtWidgets.QWidget()
        widget_sell.setObjectName('checkbox')
        checkbox_sell = QtWidgets.QCheckBox()
        setattr(self, f'{item.name}_checkbox_sell', checkbox_sell)
        
        self.set_checkbox_state(item)
        
        layout_sell = QtWidgets.QHBoxLayout(widget_sell)
        layout_sell.addWidget(checkbox_sell)
        layout_sell.setAlignment(QtCore.Qt.AlignCenter)

        button_delete = QtWidgets.QPushButton()
        button_delete.setText('Delete')
        button_delete.setObjectName('delete-btn')
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
        
    def open_url(self, item):
        if item.column() == 0 and item.row() > 0:
            item = get_item(item.text())
            webbrowser.open(item.steam_url)
    
    def change_all_states(self, state, column):
        set_buy_items(state) if column == 'buy' else set_sell_items(state)
        items = get_items()
            
        for item in items:
            checkbox = getattr(self, f'{item.name}_checkbox_{column}')
            checkbox.setChecked(item.buy_item if column == 'buy' else item.sell_item)
        
    def delete_item(self, name):
        row = self.table.currentRow()
        delete_item(name)
        self.table.removeRow(row)
        
    def delete_items(self):
        delete_items()
        self.table.setRowCount(1)
            
    def action_all(self):
        widget_buy = QtWidgets.QWidget()
        widget_buy.setObjectName('checkbox')
        
        self.checkbox_buy_all = QtWidgets.QCheckBox()
        self.checkbox_buy_all.clicked.connect(lambda: self.change_all_states(self.checkbox_buy_all.isChecked(), 'buy'))
        self.checkbox_buy_all.setChecked(check_buy_items())
        
        layout_buy = QtWidgets.QHBoxLayout(widget_buy)
        layout_buy.addWidget(self.checkbox_buy_all)
        layout_buy.setAlignment(QtCore.Qt.AlignCenter)

        widget_sell = QtWidgets.QWidget()
        widget_sell.setObjectName('checkbox')
        
        self.checkbox_sell_all = QtWidgets.QCheckBox()
        self.checkbox_sell_all.clicked.connect(lambda: self.change_all_states(self.checkbox_sell_all.isChecked(), 'sell'))
        self.checkbox_sell_all.setChecked(check_sell_items())
        
        layout_sell = QtWidgets.QHBoxLayout(widget_sell)
        layout_sell.addWidget(self.checkbox_sell_all)
        layout_sell.setAlignment(QtCore.Qt.AlignCenter)

        button_delete = QtWidgets.QPushButton()
        button_delete.setText('Delete')
        button_delete.setObjectName('delete-btn')
        button_delete.clicked.connect(lambda: self.delete_items())

        amount = QtWidgets.QTableWidgetItem('0')
        amount.setTextAlignment(QtCore.Qt.AlignCenter)

        purschase = QtWidgets.QTableWidgetItem('0.0')
        purschase.setTextAlignment(QtCore.Qt.AlignCenter)

        selling = QtWidgets.QTableWidgetItem('0.0')
        selling.setTextAlignment(QtCore.Qt.AlignCenter)

        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem('*'))
        self.table.setItem(0, 1, amount)
        self.table.setCellWidget(0, 2, widget_buy)
        self.table.setCellWidget(0, 3, widget_sell)
        self.table.setItem(0, 4, purschase)
        self.table.setItem(0, 5, selling)
        self.table.setCellWidget(0, 6, button_delete)

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
        self.add_item_btn.clicked.connect(self.open_add_item_window)
        self.buttons_layout.addWidget(self.add_item_btn)
        
        self.update_table_btn = QtWidgets.QPushButton(self.buttons_area)
        self.update_table_btn.setObjectName('default-btn')
        self.update_table_btn.setText('Update Table')
        self.update_table_btn.clicked.connect(self.update_table)
        self.buttons_layout.addWidget(self.update_table_btn)
    
    def update_table(self):
        dlg = QtWidgets.QFileDialog()
        path_to_json_file = dlg.getOpenFileName(
            self.page,
            'Open file', 
            os.getcwd(), 
            'JSON document (*.json)'
        )[0]
        
        if path_to_json_file != '' and self.validate_items_file(path_to_json_file):
            delete_items()
            self.table.setRowCount(1)
            add_items(path_to_json_file)
            items = get_items()
            for item in items:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.add_item_to_table(item, row)
    
    def validate_items_file(self, path):
        with open(path) as items_json:
            items = json.load(items_json)
        
        for item in items:
            if len(item) != 3 or list(item.keys()) != ['name', 'game', 'url']:
                return False 
            
        return True
    
    def open_add_item_window(self):
        self.window_add_item = AddItemModalWindow(self)
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
        self.log_box.widget.setStyleSheet('color: red;')
        logging.getLogger().addHandler(self.log_box)
        logging.getLogger().setLevel(logging.INFO)


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
        