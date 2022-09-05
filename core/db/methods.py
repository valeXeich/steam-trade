import json

from core.utils import parse
from .db import session
from .models import User, Item, Game


def add_user(account_name, cookies):
    user = User(
        account_name=account_name,
        avatar='/some/path',
        session_id=cookies['sessionid'],
        steam_id=cookies['steam_id'],
        oauth_token=cookies['oauth_token'],
        shared_secret='blablabla', 
        identity_secret='blablabla',
        revocation_code='12345',
        device_id=None,
    )
    session.add(user)
    session.commit()
    
def is_user_login():
    user = session.query(User).filter(User.is_login == 1)
    return session.query(User.is_login).filter(user.exists()).scalar()

def get_user():
    user = session.query(User).filter(User.is_login == 1).first()
    return user

def get_item(name):
    item = session.query(Item).filter(Item.name==name).first()
    return item

def get_items():
    items = session.query(Item).all()
    return items

def add_item(url, name=None, game_id=None):
    if name is None or game_id is None:
        name, game_id = parse(url)
    games = {
        '730': 'CS:GO',
        '570': 'DOTA2',
        '440': 'TF2',
        '753': 'STEAM',
    }
    game = session.query(Game).filter(Game.name==games[game_id]).first()
    item = Item(name=name, steam_url=url, game=game.pk)
    session.add(item)
    session.commit()

def add_items(path):
    with open(path) as items_json:
        items = json.load(items_json)
    for item in items:
        add_item(item['url'], name=item['name'], game_id=item['game'])
        
def delete_item(name):
    item = session.query(Item).filter(Item.name==name).first()
    session.delete(item)
    session.commit()
    
def delete_items():
    session.query(Item).delete()
    session.commit()
    
def set_buy_item(name):
    item = session.query(Item).filter(Item.name==name).first()
    item.buy_item = not item.buy_item
    session.commit()

def set_buy_items(state):
    items = session.query(Item).all()
    for item in items:
        item.buy_item = True if state else False
    session.commit()
    
def check_buy_items():
    items = session.query(Item.buy_item).all()
    return all([item[0] for item in items])

def set_sell_item(name):
    item = session.query(Item).filter(Item.name==name).first()
    item.sell_item = not item.sell_item
    session.commit()

def set_sell_items(state):
    items = session.query(Item).all()
    for item in items:
        item.sell_item = True if state else False
    session.commit()
    
def check_sell_items():
    items = session.query(Item.sell_item).all()
    return all([item[0] for item in items])

def set_amount(name, value):
    item = session.query(Item).filter(Item.name==name).first()
    item.amount = value
    session.commit()

def set_amount_all(value):
    items = session.query(Item).all()
    for item in items:
        item.amount = value
    session.commit()
    
def set_buy_price(name, value):
    item = session.query(Item).filter(Item.name==name).first()
    item.buy_price = value
    session.commit()

def set_buy_price_all(value):
    items = session.query(Item).all()
    for item in items:
        item.buy_price = value
    session.commit()  
  
def set_sell_price(name, value):
    item = session.query(Item).filter(Item.name==name).first()
    item.sell_price = value
    session.commit()

def set_sell_price_all(value):
    items = session.query(Item).all()
    for item in items:
        item.sell_price = value
    session.commit() 
    