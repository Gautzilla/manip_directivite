from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, VARCHAR, DATE, FLOAT, BOOLEAN
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

Base = declarative_base()
Session = None

def initialize_db():    
    global Session    
    engine = create_engine('sqlite:///model/manip_directivite.db', echo = True)
    Base.metadata.create_all(bind = engine)
    Session = sessionmaker(bind = engine)

class Room(Base):
    __tablename__ = 'rooms'

    id = Column('id', Integer, primary_key = True)
    name = Column('name', VARCHAR(200))
    rt_60 = Column('rt_60', FLOAT)

    def __init__(self, name: str, rt_60: float):
        self.name = name
        self.rt_60 = rt_60

def create_new_room(name: str, rt_60: float):
    room = Room(name, rt_60)
    add_to_db(room)

class Condition(Base):
    __tablename__ = 'conditions'

    id = Column('id', Integer, primary_key = True)
    distance = Column('distance', Integer)
    angle = Column('angle', VARCHAR(50))
    movement = Column('movement', BOOLEAN)
    source = Column('source', VARCHAR(50))

    def __init__(self, distance: int, angle: str, movement: bool, source: str):
        self.distance = distance
        self.angle = angle
        self.movement = movement
        self.source = source

class Sentence(Base):
    __tablename__ = 'sentences'

    id = Column('id', Integer, primary_key = True)
    text = Column('text', VARCHAR(500))
    amplitude = Column('text', VARCHAR(50))

    def __init__(self, text: str, amplitude: str):
        self.text = text
        self.amplitude = amplitude

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column('id', Integer, primary_key = True)
    plausibility = Column('plausibility', FLOAT)
    source_width = Column('source_width', FLOAT)

    def __init__(self, plausibility: float, source_width: float):
        self.plausibility = plausibility
        self.source_width = source_width

class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key = True)
    first_name = Column('first_name', VARCHAR(200))
    last_name = Column('last_name', VARCHAR(200))
    birth_date = Column('birth_date', DATE)

    def __init__(self, first_name: str, last_name: str, birth_date: datetime):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

def create_new_user(first_name: str, last_name: str, birth_date: datetime):
    user = User(first_name, last_name, birth_date)
    add_to_db(user)

def add_to_db(object):
    global Session
    session = Session()
    try:
        session.add(object)
        session.commit()
    finally:
        session.close()