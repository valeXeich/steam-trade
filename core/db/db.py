from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///test.db', connect_args={'check_same_thread': False})
dbsession = Session(engine)
