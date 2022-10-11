from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import PATH_TO_DB

db_path = f'{PATH_TO_DB}'
engine = create_engine(f'sqlite:///{db_path}', connect_args={'check_same_thread': False})
dbsession = Session(engine)
