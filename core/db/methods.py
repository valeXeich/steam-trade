import json

from steamlib.utils import get_item_name_id_by_url
from core.utils import parse, get_avatar_url
from .db import dbsession
from .models import BuyerToReceive, ItemNameId, User, Item, Game

def add_user(account_name, session):
    cookies = session.cookies.get_dict()
    user = User(
        account_name=account_name,
        avatar=get_avatar_url(session),
        session_id=cookies['sessionid'],
        steam_id=cookies['steam_id'],
        oauth_token=cookies['oauth_token'],
    )
    dbsession.add(user)
    dbsession.commit()
    
def is_user_login():
    user = dbsession.query(User).filter(User.is_login == 1)
    return dbsession.query(User.is_login).filter(user.exists()).scalar()

def get_user():
    user = dbsession.query(User).filter(User.is_login == 1).first()
    return user

def set_user_avatar(link):
    user = dbsession.query(User).filter(User.is_login == 1) .first()
    user.avatar = link
    dbsession.commit()

def get_item(name):
    item = dbsession.query(Item).filter(Item.name==name).first()
    return item

def get_items():
    items = dbsession.query(Item).all()
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
    game = dbsession.query(Game).filter(Game.name==games[game_id]).first()
    item = Item(name=name, steam_url=url, game=game.pk)
    dbsession.add(item)
    dbsession.commit()
    return item

def add_items(path):
    with open(path) as items_json:
        items = json.load(items_json)
    for item in items:
        add_item(item['url'], name=item['name'], game_id=item['game'])
        
def delete_item(name):
    item = dbsession.query(Item).filter(Item.name==name).first()
    dbsession.delete(item)
    dbsession.commit()
    
def delete_items():
    dbsession.query(Item).delete()
    dbsession.commit()
    
def set_buy_item(name):
    item = dbsession.query(Item).filter(Item.name==name).first()
    item.buy_item = not item.buy_item
    dbsession.commit()

def set_buy_items(state):
    items = dbsession.query(Item).all()
    for item in items:
        item.buy_item = True if state else False
    dbsession.commit()
    
def check_buy_items():
    items = dbsession.query(Item.buy_item).all()
    return all([item[0] for item in items])

def set_sell_item(name):
    item = dbsession.query(Item).filter(Item.name==name).first()
    item.sell_item = not item.sell_item
    dbsession.commit()

def set_sell_items(state):
    items = dbsession.query(Item).all()
    for item in items:
        item.sell_item = True if state else False
    dbsession.commit()
    
def check_sell_items():
    items = dbsession.query(Item.sell_item).all()
    return all([item[0] for item in items])

def set_amount(name, value):
    item = dbsession.query(Item).filter(Item.name==name).first()
    item.amount = value
    dbsession.commit()

def set_amount_all(value):
    items = dbsession.query(Item).all()
    for item in items:
        item.amount = value
    dbsession.commit()
    
def set_buy_price(name, value):
    item = dbsession.query(Item).filter(Item.name==name).first()
    item.buy_price = value
    dbsession.commit()

def set_buy_price_all(value):
    items = dbsession.query(Item).all()
    for item in items:
        item.buy_price = value
    dbsession.commit()  
  
def set_sell_price(name, value):
    item = dbsession.query(Item).filter(Item.name==name).first()
    item.sell_price = value
    dbsession.commit()

def set_sell_price_all(value):
    items = dbsession.query(Item).all()
    for item in items:
        item.sell_price = value
    dbsession.commit()

def load_item_name_id(path):
    with open(path) as items_json:
        items = json.load(items_json)
    for item in items:
        item_name_id = ItemNameId(name=item, item_nameid=items[item]['item_nameid'])
        dbsession.add(item_name_id)
    dbsession.commit()

def load_buyer_to_receive(path):
    with open(path) as buyer_to_receive_json:
        buyer_to_receive = json.load(buyer_to_receive_json)
    for buyer_pays, you_receive in buyer_to_receive.items():
        obj = BuyerToReceive(buyer_pays=buyer_pays, you_receive=you_receive)
        dbsession.add(obj)
    dbsession.commit()

def get_item_nameid(item):
    item_name_id = dbsession.query(ItemNameId).filter(ItemNameId.name == item.name).first()
    if item_name_id is None:
        item_id = get_item_name_id_by_url(item.steam_url)
        item_name_id = ItemNameId(name=item.name, item_nameid=item_id)
        dbsession.add(item_name_id)
        dbsession.commit()
        return item_name_id.item_nameid
    return item_name_id.item_nameid

def get_game_by_pk(pk):
    game = dbsession.query(Game).filter(Game.pk == pk).first()
    return game

def get_items_sell(analysis=False):
    items = dbsession.query(Item).filter(Item.sell_item == True, Item.analysis == analysis).all()
    return items

def get_items_buy(analysis=False):
    items = dbsession.query(Item).filter(Item.buy_item == True, Item.analysis == analysis).all()
    return items

def get_you_receive(buyer_pays):
    price = dbsession.query(BuyerToReceive).filter(BuyerToReceive.buyer_pays == buyer_pays).first()
    return price.you_receive

def delete_bad_items(items):
    for item in items:
        dbsession.delete(item)
    dbsession.commit()