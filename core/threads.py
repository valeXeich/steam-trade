import time

from PyQt5 import QtCore
from steamlib.models import Currency
from .db.methods import get_user
from .market import Market


class ProgressBarThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)

    def __init__(self, market, buy_orders):
        super().__init__()
        self.market = market
        self.buy_orders = buy_orders
        self.count = len(buy_orders)

    def run(self):
        for n, order_id in zip(range(self.count), self.buy_orders):
            self.market.cancel_buy_order(order_id)
            self.signal.emit(n)


class DeleteUnprofitableThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)
    delete_signal = QtCore.pyqtSignal(list)

    def __init__(self, market, items):
        super().__init__()
        self.market = market
        self.items = items
        self.buy_orders = self.market.get_market_listings()['buy_orders']
        self.count = len(items)
    
    def run(self):
        bad_items = []
        for n, item in zip(range(self.count), self.items):
            bad_item = self.market.delete_unprofitable_item(item, Currency.UAH, self.buy_orders)
            if bad_item is not None:
                bad_items.append(bad_item)
            self.signal.emit(n)
        self.delete_signal.emit(bad_items)


class SteamGuardTimer(QtCore.QThread):
    counter = QtCore.pyqtSignal(int)
    
    def __init__(self, guard):
        super().__init__()
        self.guard = guard
    
    def run(self):
        start = self.start_value
        while True:
            start -= 1
            time.sleep(1)
            self.counter.emit(start)
            if start == 0:
                start = 30
    
    @property
    def start_value(self):
        timestamp = self.guard._get_time()
        return 30 - timestamp % 60 % 30
        

class Start(QtCore.QThread):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.active = False
        self.user = get_user()
    
    @property
    def secrets(self):
        data = {}
        if self.user.identity_secret:
            data['identity_secret'] = self.user.identity_secret
        if self.user.shared_secret:
            data['shared_secret'] = self.user.shared_secret
        return data

    def run(self):
        self.active = not self.active
        market = Market(self.session, self.secrets)
        while self.active:
            market.create_buy_orders_analysis(Currency.UAH)
            market.create_sell_orders_analysis(Currency.UAH)
            time.sleep(30)
            
    def stop(self):
        self.active = not self.active
        self.terminate()
            