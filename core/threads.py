from PyQt5 import QtCore

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