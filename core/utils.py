from steamlib.utils import get_lowest_sell_order, get_highest_buy_order
from steamlib.models import APIEndpoint
from db.db import session
from db.models import BuyerToReceive
from decimal import Decimal
import urllib
from bs4 import BeautifulSoup

def get_price(currency, item_name_id, method):
    if method == 'sell':
        last_sell_order = get_lowest_sell_order(currency, item_name_id)['full']
        obj = session.query(BuyerToReceive).filter(BuyerToReceive.buyer_pays == last_sell_order).first()
        result = str(round(Decimal(obj.you_receive) - Decimal(0.01), 2)).replace('.', '')
        if result[0] == '0':
            return result[1:]
        return result
    else:
        highest_buy_order = int(get_highest_buy_order(currency, item_name_id)['pennies']) + 1
        return highest_buy_order

def check_quantity(buy_orders, items, cancel_order):
    for order in buy_orders:
        for item in items:
            if order['name'] == item.name and order['count'] != item.amount:
                cancel_order(order)

def get_two_last_sell_orders(currency ,item_name_id, session):
    params = {
        'item_nameid': item_name_id,
        'currency': currency,
        'two_factor': 0,
        'language': 'english',
        'country': 'UA',
    }
    response = session.get(f'{APIEndpoint.COMMUNITY_URL}market/itemordershistogram', params=params).json()
    first_price = response['sell_order_graph'][0][0]
    second_price = response['sell_order_graph'][1][0]
    return {'first_price': first_price, 'second_price': second_price}

def get_buy_order_id(buy_orders, item):
    for order in buy_orders:
        if order['name'] == item.name:
            return order

def parse(url):
    url = url.split('/')
    name = urllib.parse.unquote(url[6])
    game_id = url[5]
    return name, game_id

def get_avatar_url(session):
    content = session.get('https://store.steampowered.com/').text
    soup = BeautifulSoup(content, 'html.parser')
    link = soup.find('span', {'class': 'pulldown'}).find('img', {'class': 'foryou_avatar'}).attrs['src']
    return f"{link[:-4].replace('akamai', 'cloudflare')}_full.jpg"