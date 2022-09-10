from steamlib.models import Game as game, Currency
from steamlib.market import SteamMarket

from db.db import session as s
from db.models import BuyerToReceive, Item, ItemNameId, Game
from login import do_login
from utils import get_price, check_quantity, get_two_last_sell_orders, get_buy_order_id


class Market(SteamMarket):

    def get_inventories(self):
        inventories = {
            'CS:GO': self.get_inventory(game.CSGO),
            'DOTA2': self.get_inventory(game.DOTA2),
            # 'TF2': self.get_inventory(game.TF2)
        }
        return inventories
    
    def get_asset_id(self, item, inventories, assets):
        game = s.query(Game).filter(Game.pk == item.game).first()
        for item_ in inventories[game.name]:
            if item_['market_name'] == item.name and item_['assetid'] not in assets:
                assets.append(item_['assetid'])
                return item_['assetid']

    def create_sell_orders_analysis(self, currency, game):
        assets = []
        inventories = self.get_inventories()
        items = s.query(Item).filter(Item.sell_item == True).all()
        for item in items:
            item_name_id = s.query(ItemNameId).filter(ItemNameId.name == item.name).first().item_nameid
            price = get_price(currency, item_name_id, 'sell')
            asset_id = self.get_asset_id(item, inventories, assets)
            self.create_sell_order(game, 1, price, asset_id)
    
    # need test
    def create_buy_orders_analysis(self, currency, game):
        buy_orders = self.get_market_listings()['buy_orders']
        items = s.query(Item).filter(Item.buy_item == True).all()
        check_quantity(buy_orders, items, self.cancel_buy_order)
        for item in items:
            item_name_id = s.query(ItemNameId).filter(ItemNameId.name == item.name).first().item_nameid
            price = get_price(currency, item_name_id, 'buy')
            self.create_buy_order(currency, game, item.name, price, item.amount)
    
    def create_sell_orders(self, game):
        assets = []
        inventories = self.get_inventories()
        items = s.query(Item).filter(Item.sell_item == True).all()
        for item in items:
            asset_id = self.get_asset_id(item, inventories, assets)
            price = s.query(BuyerToReceive).filter(BuyerToReceive.buyer_pays).first()
            self.create_sell_order(game, 1, price.you_receive, asset_id)
    
    def create_buy_orders(self, currency, game):
        buy_orders = self.get_market_listings()['buy_orders']
        items = s.query(Item).filter(Item.buy_item == True).all()
        check_quantity(buy_orders, items, self.cancel_buy_order)
        for item in items:
            self.create_buy_order(currency, game, item.name, item.buy_price, item.amount)
    
    # need test
    def delete_unprofitable_items(self, currency):
        items = s.query(Item).all()
        buy_orders = self.get_market_listings()['buy_orders']
        for item in items:
            item_name_id = s.query(ItemNameId).filter(ItemNameId.name == item.name).first().item_nameid
            last_two_orders = get_two_last_sell_orders(currency, item_name_id, self._session)
            price = get_price(currency, item_name_id, 'buy')
            first_receive = s.query(BuyerToReceive).filter(BuyerToReceive.buyer_pays == last_two_orders['first_price']).first()
            second_receive = s.query(BuyerToReceive).filter(BuyerToReceive.buyer_pays == last_two_orders['second_price']).first()
            result = float(first_receive.you_receive) - (price / 100) < 0 and float(second_receive.you_receive) - (price / 100) < 0
            if result:
                buy_order_id = get_buy_order_id(buy_orders, item)
                self.cancel_buy_order(buy_order_id)
                s.delete(item)
        s.commit()




session = do_login()

market = Market(session)
market.delete_unprofitable_items(Currency.UAH)


