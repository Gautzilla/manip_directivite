from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_PATH = 'sqlite:///data/manip_directivite.db'
Base = declarative_base()

from model.models import *

engine = create_engine(DATABASE_PATH, echo = False)
Base.metadata.drop_all(bind = engine)
Base.metadata.create_all(bind = engine)
Session = sessionmaker(bind = engine)


