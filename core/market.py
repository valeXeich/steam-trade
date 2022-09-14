from steamlib.models import Game
from steamlib.market import SteamMarket
import logging

from .db.methods import get_item_nameid, get_game_by_pk, get_items_sell, get_items_buy, get_you_receive, get_items, delete_bad_items
from .utils import get_game_by_id, get_price, check_quantity, get_two_last_sell_orders, get_buy_order_id, item_in_orders, convert_to_penny


class Market(SteamMarket):

    def get_inventories(self):
        inventories = {
            'CS:GO': self.get_inventory(Game.CSGO),
            # 'DOTA2': self.get_inventory(Game.DOTA2),
            # 'TF2': self.get_inventory(Game.TF2)
        }
        return inventories
    
    def get_asset_id(self, item, inventories, assets):
        game = get_game_by_pk(item.game)
        for item_ in inventories[game.name]:
            if item_['market_name'] == item.name and item_['assetid'] not in assets:
                assets.append(item_['assetid'])
                return item_['assetid']

    def create_sell_orders_analysis(self, currency):
        assets = []
        inventories = self.get_inventories()
        items = get_items_sell(analysis=True)
        for item in items:
            asset_id = self.get_asset_id(item, inventories, assets)
            if asset_id is None:
                continue
            item_name_id = get_item_nameid(item)
            price = get_price(currency, item_name_id, 'sell')
            game = get_game_by_id(item.game)
            self.create_sell_order(game, 1, price, asset_id, item.analysis)
            logging.info(f'{item.name} on sale for {price / 100}')
    
    def create_buy_orders_analysis(self, currency):
        buy_orders = self.get_market_listings()['buy_orders']
        items = get_items_buy(analysis=True)
        check_quantity(buy_orders, items, self.cancel_buy_order)
        for item in items:
            if not item_in_orders(buy_orders, item):
                item_name_id = get_item_nameid(item)
                price = get_price(currency, item_name_id, 'buy')
                game = get_game_by_id(item.game)
                self.create_buy_order(currency, game, item.name, price, item.amount)
                logging.info(f'{item.name} order placed {price / 100}')
    
    def create_sell_orders(self):
        assets = []
        inventories = self.get_inventories()
        items = get_items_sell()
        for item in items:
            asset_id = self.get_asset_id(item, inventories, assets)
            you_receive = get_you_receive(item.sell_price)
            price = convert_to_penny(you_receive)
            game = get_game_by_id(item.game)
            self.create_sell_order(game, 1, price, asset_id, item.analysis)
            logging.info(f'{item.name} on sale for {price / 100}')
    
    def create_buy_orders(self, currency):
        buy_orders = self.get_market_listings()['buy_orders']
        items = get_items_buy()
        check_quantity(buy_orders, items, self.cancel_buy_order)
        for item in items:
            if not item_in_orders(buy_orders, item):
                game = get_game_by_id(item.game)
                price = convert_to_penny(item.buy_price)
                self.create_buy_order(currency, game, item.name, price, item.amount)
                logging.info(f'{item.name} order placed {price / 100}')
    
    # need test
    def delete_unprofitable_items(self, currency):
        items = get_items()
        bad_items = []
        buy_orders = self.get_market_listings()['buy_orders']
        for item in items:
            item_name_id = get_item_nameid(item)
            last_two_orders = get_two_last_sell_orders(currency, item_name_id, self._session)
            price = get_price(currency, item_name_id, 'buy')
            first_receive = get_you_receive(last_two_orders['first_price'])
            second_receive = get_you_receive(last_two_orders['second_price'])
            result = float(first_receive) - (price / 100) < 0 and float(second_receive) - (price / 100) < 0
            if result:
                buy_order_id = get_buy_order_id(buy_orders, item)
                if buy_order_id is not None:
                    self.cancel_buy_order(buy_order_id)
                bad_items.append(item)
        delete_bad_items(bad_items)
