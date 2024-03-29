import urllib
from decimal import Decimal
from typing import List

import requests
from bs4 import BeautifulSoup
from core.db.db import dbsession
from steamlib.models import APIEndpoint
from steamlib.models import Game as GameOptions
from steamlib.utils import get_highest_buy_order, get_lowest_sell_order

from .db.models import BuyerToReceive, Game, Item


def get_log_ex_message(ex):
    if '107' in str(ex):
        return "User doesn't have enough money to buy item"
    if '25' in str(ex):
        return str(ex).split('.')[1]
    

def get_correct_price(price: str) -> str:
    data = str(price).split(".")
    if len(data) == 1:
        price = str(price) + ".00"
    elif len(data[-1]) == 1:
        price = str(price) + "0"
    return price


def get_correct_last_sell_order(currency, item_name_id: str) -> str:
    last_sell_order = get_lowest_sell_order(currency, item_name_id)["full"]
    return get_correct_price(last_sell_order)


def get_price(currency: dict, item_name_id: str, method: str) -> str:
    if method == "sell":
        last_sell_order = get_correct_last_sell_order(currency, item_name_id)
        obj = (
            dbsession.query(BuyerToReceive)
            .filter(BuyerToReceive.buyer_pays == last_sell_order)
            .first()
        )
        result = str(round(Decimal(obj.you_receive) - Decimal(0.01), 2)).replace(
            ".", ""
        )
        if result[0] == "0":
            return result[1:]
        return int(result)
    else:
        highest_buy_order = (
            int(get_highest_buy_order(currency, item_name_id)["pennies"]) + 1
        )
        return highest_buy_order


def check_quantity(buy_orders: dict, items: List[Item], cancel_order) -> None:
    for order in buy_orders:
        for item in items:
            if (
                buy_orders[order]["name"] == item.name
                and int(buy_orders[order]["count"]) != item.amount
            ):
                cancel_order(order)


def get_two_last_sell_orders(
    currency, item_name_id: str, session: requests.Session
) -> dict:
    params = {
        "item_nameid": item_name_id,
        "currency": currency,
        "two_factor": 0,
        "language": "english",
        "country": "UA",
    }
    response = session.get(
        f"{APIEndpoint.COMMUNITY_URL}market/itemordershistogram", params=params
    ).json()
    first_price = get_correct_price(response["sell_order_graph"][0][0])
    second_price = get_correct_price(response["sell_order_graph"][1][0])
    return {"first_price": first_price, "second_price": second_price}


def get_buy_order_id(buy_orders: dict, item: Item) -> int:
    for order in buy_orders:
        if buy_orders[order]["name"] == item.name:
            return order


def parse(url: str) -> tuple:
    url = url.split("/")
    name = urllib.parse.unquote(url[6])
    game_id = url[5]
    return name, game_id


def get_avatar_url(session: requests.Session) -> str:
    content = session.get("https://store.steampowered.com/").text
    soup = BeautifulSoup(content, "html.parser")
    try:
        link = (
            soup.find("span", {"class": "pulldown"})
            .find("img", {"class": "foryou_avatar"})
            .attrs["src"]
        )
    except AttributeError:
        return "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b5/b5bd56c1aa4644a474a2e4972be27ef9e82e517e_full.jpg"
    return f"{link[:-4].replace('akamai', 'cloudflare')}_full.jpg"


def get_game_by_id(game_pk: int) -> dict:
    game = dbsession.query(Game).filter(Game.pk == game_pk).first()
    games = {
        "CS:GO": GameOptions.CSGO,
        "DOTA2": GameOptions.DOTA2,
        "TF2": GameOptions.TF2,
    }
    return games[game.name]


def item_in_orders(buy_orders: dict, item: Item) -> bool:
    for order in buy_orders:
        if buy_orders[order]["name"] == item.name:
            return True
    return False


def convert_to_penny(price: str) -> str:
    return str(int(float(price) * 100)).replace(".", "")
