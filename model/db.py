from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, VARCHAR, DATE, FLOAT, BOOLEAN
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
import pandas as pd

SENTENCES_CSV_FILE = r'data\sentences.csv'
DATABASE_PATH = 'sqlite:///model/manip_directivite.db'
Base = declarative_base()
Session = None

def initialize_db():    
    global Session    
    engine = create_engine(DATABASE_PATH, echo = True)
    Base.metadata.create_all(bind = engine)
    Session = sessionmaker(bind = engine)
    add_rooms()
    import_data()

def add_rooms():
    clous = Room(0, 'CLOUS', 0.5)
    suaps = Room(1, 'SUAPS', 2.)
    for room in [clous, suaps] :
        add_to_db(room)

def import_data():
    recordings = pd.read_csv(SENTENCES_CSV_FILE)
    recordings.head()
    pass

class IndependantVariable(Base):
    __tablename__ = 'independant_variables'

    id = Column('id', Integer, primary_key = True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    conditions_id = Column(Integer, ForeignKey('conditions.id'))
    sentence_id = Column(Integer, ForeignKey('sentences.id'))

    def __init__(self, room_id, conditions_id, sentence_id):
        self.room_id = room_id
        self.conditions_id = conditions_id
        self.sentence_id = sentence_id

class Trial(Base):
    __tablename__ = 'trials'

    id = Column('id', Integer, primary_key = True)
    index = Column('index', Integer)
    repetition = Column('repetition', Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    independant_variable_id = Column(Integer, ForeignKey('independant_variables.id'))
    rating_id = Column(Integer, ForeignKey('ratings.id'))
    audio_file = Column('audio_file', VARCHAR(500))

    def __init__(self, index, repetition, user_id, independant_variable_id):
        self.index = index
        self.repetition = repetition
        self.user_id = user_id
        self.independant_variable_id = independant_variable_id
        # audio_file path can be created here 

class Room(Base):
    __tablename__ = 'rooms'

    id = Column('id', Integer, primary_key = True)
    name = Column('name', VARCHAR(200))
    rt_60 = Column('rt_60', FLOAT)

    def __init__(self, id: Integer, name: str, rt_60: float):
        self.id = id
        self.name = name
        self.rt_60 = rt_60

class Condition(Base):
    __tablename__ = 'conditions'

    id = Column('id', Integer, primary_key = True)
    distance = Column('distance', Integer)
    angle = Column('angle', VARCHAR(50))
    movement = Column('movement', BOOLEAN)
    source = Column('source', VARCHAR(50))

    def __init__(self, id: int, distance: int, angle: str, movement: bool, source: str):
        self.id = id
        self.distance = distance
        self.angle = angle
        self.movement = movement
        self.source = source

class Sentence(Base):
    __tablename__ = 'sentences'

    id = Column('id', Integer, primary_key = True)
    text = Column('text', VARCHAR(500))
    amplitude = Column('amplitude', VARCHAR(50))

    def __init__(self, id: int, text: str, amplitude: str):
        self.id = id
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
    except:
        print(f'cant add {object}')
    finally:
        session.close()