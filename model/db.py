from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, VARCHAR, DATE
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

Base = declarative_base()

def initialize_db():    
    engine = create_engine('sqlite:///model/manip_directivite.db', echo = True)
    Base.metadata.create_all(bind = engine)

class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key = True)
    first_name = Column('first_name', VARCHAR(200))
    last_name = Column('last_name', VARCHAR(200))
    birth_date = Column('birth_date', DATE)

    def __init__(self, first_name, last_name, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date