from .market import Market
from steamlib.models import Currency
from PyQt5.QtCore import QThread
import time
from .db.methods import get_user

class MarketThread(QThread):
    def __init__(self, session):
        super().__init__()
        self.user = get_user()
        self.market = Market(session, self.secrets)
    
    @property
    def secrets(self):
        data = {}
        if self.user.identity_secret:
            data['identity_secret'] = self.user.identity_secret
        if self.user.shared_secret:
            data['shared_secret'] = self.user.shared_secret
        return data
    
    def run(self):
        self.market.create_buy_orders_analysis(Currency.UAH)
        self.market.create_sell_orders_analysis(Currency.UAH)

class Start(QThread):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.active = False
        self.market = MarketThread(self.session)
    
    def run(self):
        self.active = not self.active
        self.market.market.stop = False
        while self.active:
            self.market.start()
            self.market.wait()
            
    def stop(self):
        self.active = not self.active
        self.market.market.stop = True
        self.wait()

