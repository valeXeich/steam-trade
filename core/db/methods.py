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
        steam_login= cookies['steamLogin'],
        steam_login_secure=cookies['steamLoginSecure'],
        steam_machine_auth=cookies[f"steamMachineAuth{cookies['steam_id']}"],
        shared_secret='blablabla', 
        identity_secret='blablabla',
        revocation_code='12345',
        device_id=None,
    )
    session.add(user)
    session.commit()
    
def is_user_login():
    user = session.query(User).filter(User.is_loggin == 1)
    return session.query(User.is_loggin).filter(user.exists()).scalar()

def get_user():
    user = session.query(User).filter(User.is_loggin == 1).first()
    return user

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

def set_buy_items():
    items = session.query(Item).all()
    for item in items:
        item.buy_item = not item.buy_item
    session.commit()
