import json
from typing import List, Optional

import requests
from core.utils import get_avatar_url, parse
from steamlib.utils import get_item_name_id_by_url

from .db import dbsession, engine
from .models import Base, BuyerToReceive, Game, Item, ItemNameId, Setting, User


def create_db():
    Base.metadata.create_all(engine)
    games = dbsession.query(Game).count()
    if games == 0:
        add_games()


def add_games():
    cs, dota, tf = Game(name="CS:GO"), Game(name="DOTA2"), Game(name="TF2")
    dbsession.add_all([cs, dota, tf])
    dbsession.commit()


def add_user(account_name: str, session: requests.Session, is_login: bool = True):
    cookies = session.cookies.get_dict()
    user = User(
        account_name=account_name,
        avatar=get_avatar_url(session),
        session_id=cookies["sessionid"],
        steam_id=cookies["steam_id"],
        oauth_token=cookies["oauth_token"],
        is_login=is_login,
    )
    dbsession.add(user)
    dbsession.commit()
    setting = Setting(user=user.pk)
    dbsession.add(setting)
    dbsession.commit()


def is_user_login() -> bool:
    user = dbsession.query(User).filter(User.is_login == 1).first()
    return True if user is not None else False


def get_user() -> User:
    user = dbsession.query(User).filter(User.is_login == 1).first()
    return user


def get_users() -> List[User]:
    users = dbsession.query(User).all()
    return users


def get_last_added_user() -> User:
    user = dbsession.query(User).order_by(User.pk.desc()).first()
    return user


def delete_user(user: User):
    delete_items(user)
    delete_setting(user)
    dbsession.delete(user)
    dbsession.commit()


def change_user(changed_account: User):
    current_user = get_user()
    current_user.is_login = False
    changed_account.is_login = True
    dbsession.commit()


def set_user_avatar(link: str):
    user = dbsession.query(User).filter(User.is_login == 1).first()
    user.avatar = link
    dbsession.commit()


def get_item(name: str, user: Optional[User] = None) -> Item:
    if user is None:
        user = get_user()
    item = dbsession.query(Item).filter(Item.name == name, Item.user == user.pk).first()
    return item


def get_items() -> List[Item]:
    user = get_user()
    items = dbsession.query(Item).filter(Item.user == user.pk).all()
    return items
 

def get_items_count() -> int:
    user = get_user()
    amount = dbsession.query(Item).filter(Item.user == user.pk).count()
    return amount

def add_item(
    url,
    name: Optional[str] = None,
    game_id: Optional[int] = None,
    user: Optional[User] = None,
) -> Optional[Item]:
    if name is None or game_id is None:
        name, game_id = parse(url)
    games = {
        "730": "CS:GO",
        "570": "DOTA2",
        "440": "TF2",
        "753": "STEAM",
    }

    if user is None:
        user = get_user()

    if get_item(name) is None:
        game = dbsession.query(Game).filter(Game.name == games[game_id]).first()
        item = Item(name=name, steam_url=url, game=game.pk, user=user.pk)
        dbsession.add(item)
        dbsession.commit()
        return item

    raise KeyError()


def add_items(path: str):
    user = get_user()
    with open(path) as items_json:
        items = json.load(items_json)
    for item in items:
        add_item(item["url"], name=item["name"], game_id=item["game"], user=user)


def delete_item(name: str):
    user = get_user()
    item = dbsession.query(Item).filter(Item.name == name, Item.user == user.pk).first()
    dbsession.delete(item)
    dbsession.commit()


def delete_items(user: Optional[User] = None):
    if not user:
        user = get_user()
    items = dbsession.query(Item).filter(Item.user == user.pk).all()
    for item in items:
        dbsession.delete(item)
    dbsession.commit()


def set_buy_item(name: str):
    user = get_user()
    item = dbsession.query(Item).filter(Item.name == name, Item.user == user.pk).first()
    item.buy_item = not item.buy_item
    dbsession.commit()


def set_buy_items(state: bool):
    user = get_user()
    items = dbsession.query(Item).filter(Item.user == user.pk).all()
    for item in items:
        item.buy_item = True if state else False
    dbsession.commit()


def check_buy_items() -> bool:
    user = get_user()
    items = dbsession.query(Item.buy_item).filter(Item.user == user.pk).all()
    return all([item[0] for item in items])


def set_sell_item(name: str):
    user = get_user()
    item = dbsession.query(Item).filter(Item.name == name, Item.user == user.pk).first()
    item.sell_item = not item.sell_item
    dbsession.commit()


def set_sell_items(state: bool):
    user = get_user()
    items = dbsession.query(Item).filter(Item.user == user.pk).all()
    for item in items:
        item.sell_item = True if state else False
    dbsession.commit()


def check_sell_items() -> bool:
    user = get_user()
    items = dbsession.query(Item.sell_item).filter(Item.user == user.pk).all()
    return all([item[0] for item in items])


def set_amount(name: str, value: int):
    user = get_user()
    item = dbsession.query(Item).filter(Item.name == name, Item.user == user.pk).first()
    item.amount = value
    dbsession.commit()


def set_amount_all(value: int):
    user = get_user()
    items = dbsession.query(Item).filter(Item.user == user.pk).all()
    for item in items:
        item.amount = value
    dbsession.commit()


def set_buy_price(name: str, value: float):
    user = get_user()
    item = dbsession.query(Item).filter(Item.name == name, Item.user == user.pk).first()
    item.buy_price = value
    dbsession.commit()


def set_buy_price_all(value: float):
    user = get_user()
    items = dbsession.query(Item).filter(Item.user == user.pk).all()
    for item in items:
        item.buy_price = value
    dbsession.commit()


def set_sell_price(name: str, value: float):
    user = get_user()
    item = dbsession.query(Item).filter(Item.name == name, Item.user == user.pk).first()
    item.sell_price = value
    dbsession.commit()


def set_sell_price_all(value: float):
    user = get_user()
    items = dbsession.query(Item).filter(Item.user == user.pk).all()
    for item in items:
        item.sell_price = value
    dbsession.commit()


def load_item_name_id(path: str):
    with open(path) as items_json:
        items = json.load(items_json)
    for item in items:
        item_name_id = ItemNameId(name=item, item_nameid=items[item]["item_nameid"])
        dbsession.add(item_name_id)
    dbsession.commit()


def load_buyer_to_receive(path: str):
    with open(path) as buyer_to_receive_json:
        buyer_to_receive = json.load(buyer_to_receive_json)
    for buyer_pays, you_receive in buyer_to_receive.items():
        obj = BuyerToReceive(buyer_pays=buyer_pays, you_receive=you_receive)
        dbsession.add(obj)
    dbsession.commit()


def get_item_nameid(item: Item) -> str:
    item_name_id = (
        dbsession.query(ItemNameId).filter(ItemNameId.name == item.name).first()
    )
    if item_name_id is None:
        item_id = get_item_name_id_by_url(item.steam_url)
        item_name_id = ItemNameId(name=item.name, item_nameid=item_id)
        dbsession.add(item_name_id)
        dbsession.commit()
        return item_name_id.item_nameid
    return item_name_id.item_nameid


def get_game_by_pk(pk: int) -> Game:
    game = dbsession.query(Game).filter(Game.pk == pk).first()
    return game


def get_items_sell() -> List[Item]:
    user = get_user()
    items = (
        dbsession.query(Item)
        .filter(Item.sell_item == True, Item.user == user.pk)
        .all()
    )
    return items


def get_items_buy() -> List[Item]:
    user = get_user()
    items = (
        dbsession.query(Item)
        .filter(Item.buy_item == True, Item.user == user.pk)
        .all()
    )
    return items


def get_you_receive(buyer_pays: str) -> str:
    price = (
        dbsession.query(BuyerToReceive)
        .filter(BuyerToReceive.buyer_pays == buyer_pays)
        .first()
    )
    return price.you_receive


def delete_bad_items(items: List[Item]):
    for item in items:
        dbsession.delete(item)
    dbsession.commit()


def get_secrets() -> dict:
    user = get_user()
    return {
        "shared_secret": user.shared_secret,
        "identity_secret": user.identity_secret,
        "revocation_code": user.revocation_code,
    }


def change_analysis_setting(state: bool):
    user = get_user()
    setting = dbsession.query(Setting).filter(Setting.user == user.pk).first()
    setting.analysis = state
    dbsession.commit()


def change_autoconfirm_setting(state: bool):
    user = get_user()
    setting = dbsession.query(Setting).filter(Setting.user == user.pk).first()
    setting.autoconfirm = state
    dbsession.commit()


def get_setting() -> dict:
    user = get_user()
    setting = dbsession.query(Setting).filter(Setting.user == user.pk).first()
    return {"analysis": setting.analysis, "autoconfirm": setting.autoconfirm}


def delete_setting(user: Optional[User] = None):
    if not user:
        user = get_user()
    setting = dbsession.query(Setting).filter(Setting.user == user.pk).first()
    dbsession.delete(setting)
    dbsession.commit()


def change_secrets(data: dict = {}):
    user = get_user()
    user.shared_secret = data.get("shared_secret")
    user.identity_secret = data.get("identity_secret")
    user.revocation_code = data.get("revocation_code")
    dbsession.commit()
