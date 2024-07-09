from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from os.path import exists

DATABASE_PATH = 'data/manip_directivite.db'

Base = declarative_base()

from model.models import *

engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo = False)

if not exists(DATABASE_PATH):
    Base.metadata.drop_all(bind = engine)

Base.metadata.create_all(bind = engine)
Session = sessionmaker(bind = engine)


