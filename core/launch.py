from .market import Market
from steamlib.models import Currency
from PyQt5.QtCore import QThread
import time
from .db.methods import get_user

class Start(QThread):
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
        

