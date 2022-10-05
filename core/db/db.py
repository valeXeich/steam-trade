from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

db_path = f'{Path(__file__).parent}/sta.db'
engine = create_engine(f'sqlite:///{db_path}', connect_args={'check_same_thread': False})
dbsession = Session(engine)
