import datetime

from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    
    pk = Column(Integer, primary_key=True)
    account_name = Column(String(50), unique=True, nullable=False)
    avatar = Column(String(255))
    session_id = Column(String(30), nullable=False)
    
    steam_id = Column(String(20), nullable=False)
    oauth_token = Column(String(35), nullable=False)
    
    shared_secret = Column(String(30))
    identity_secret = Column(String(30))
    revocation_code = Column(String(10))
    device_id = Column(String(60))
    is_login = Column(Boolean, default=True)
    
    def __str__(self) -> str:
        return f'User: {self.account_name}'
    

class Item(Base):
    __tablename__ = 'Item'
    
    pk = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    amount = Column(Integer, default=0)
    buy_item = Column(Boolean, default=False)
    sell_item = Column(Boolean, default=False)
    buy_price = Column(Float(precision=2), default=0)
    sell_price = Column(Float(precision=2), default=0)
    analysis = Column(Boolean, default=False)
    steam_url = Column(String(150))
    created_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    game = Column(Integer, ForeignKey('Game.pk'))
    
    def __str__(self) -> str:
        return f'Item: {self.name}'
    

class ItemNameId(Base):
    __tablename__ = 'Item_nameid'
    
    pk = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    item_nameid = Column(String(30), unique=True)

    def __str__(self) -> str:
        return f'Item: {self.name}, item_nameid: {self.item_nameid}'


class BuyerToReceive(Base):
    __tablename__ = 'Buyer_to_receive'
    
    pk = Column(Integer, primary_key=True)
    buyer_pays = Column(String(20))
    you_receive = Column(String(20))
    
    def __str__(self) -> str:
        return f'BP: {self.buyer_pays}, YR: {self.you_receive}'


class Game(Base):
    __tablename__ = 'Game'
    
    pk = Column(Integer, primary_key=True)
    name = Column(String(50))
    item = relationship('Item')
    
    def __str__(self) -> str:
        return f'Game: {self.name}'
