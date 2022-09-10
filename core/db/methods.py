from .db import session
from .models import User, Game, Item

# game = session.query(Game).filter(Game.pk == 1).first()
# item = Item(name='Desert Eagle | Поток информации', steam_url='https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Printstream%20%28Factory%20New%29', game=game.pk)
# session.add(item)
# session.commit()

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

def get_items():
    items = session.query(Item).all()
    return items

