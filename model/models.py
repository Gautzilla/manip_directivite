from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, VARCHAR, DATE, FLOAT, BOOLEAN
import datetime
from model import Base

class Recording(Base):
    __tablename__ = 'recordings'

    id = Column('id', Integer, primary_key = True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    conditions_id = Column(Integer, ForeignKey('conditions.id'))
    sentence_id = Column(Integer, ForeignKey('sentences.id'))    
    repetition = Column('repetition', Integer)
    rec_repetition = Column('rec_repetition', Integer)
    rec_repetition_rating = Column('rec_repetition_rating', Integer)
    audio_file = Column('audio_file', VARCHAR(500))

    def __init__(self, room_id, conditions_id, sentence_id, repetition, rec_repetition, rec_repetition_rating):
        self.room_id = room_id
        self.conditions_id = conditions_id
        self.sentence_id = sentence_id
        self.repetition = repetition
        self.rec_repetition = rec_repetition
        self.rec_repetition_rating = rec_repetition_rating
        # compute audio file path here

    def set_audio_file(self, file_name):
        self.audio_file = file_name

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

    def __init__(self, distance: int, angle: str, movement: bool, source: str):
        self.distance = distance
        self.angle = angle
        self.movement = movement
        self.source = source

class Sentence(Base):
    __tablename__ = 'sentences'

    id = Column('id', Integer, primary_key = True)
    text = Column('text', VARCHAR(500))
    amplitude = Column('amplitude', VARCHAR(50))

    def __init__(self, text: str, amplitude: str):
        self.text = text
        self.amplitude = amplitude

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column('id', Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    recording_id = Column(Integer, ForeignKey('recordings.id'))
    plausibility = Column('plausibility', FLOAT)
    source_width = Column('source_width', FLOAT)

    def __init__(self, plausibility: float, source_width: float, user_id: int, recording_id: int):
        self.plausibility = plausibility
        self.source_width = source_width
        self.user_id = user_id
        self.recording_id = recording_id

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