from model.models import Room, Condition, User, Sentence, Recording
import datetime

def get_room_from_recording(recording: Recording, session) -> Room:
        return session.query(Room).filter(Room.id == recording.room_id).first()

def get_room_by_attributes(room, session):
    try:
        return session.query(Room).filter(Room.name == room.name, Room.rt_60 == room.rt_60).first()
    except:
        return None    

def add_room(room, session):
    session.add(room)

def get_all_rooms(session):
    return session.query(Room).all()

def get_conditions_by_attributes(condition, session):
    try:
        return session.query(Condition).filter(Condition.distance == condition.distance, Condition.angle == condition.angle, Condition.movement == condition.movement, Condition.source == condition.source).first()
    except:
        return None  

def add_conditions(conditions, session):
    session.add(conditions)

def get_all_conditions(session):
    return session.query(Condition).all()

def get_conditions_from_recording(recording: Recording, session) -> Condition:
    return session.query(Condition).filter(Condition.id == recording.conditions_id).first()

def get_sentence_by_attributes(sentence, session):
    try:
        return session.query(Sentence).filter(Sentence.text == sentence.text, Sentence.amplitude == sentence.amplitude).first()
    except:
        return None 

def add_sentence(sentence, session):
    session.add(sentence)

def get_all_sentences(session):
    return session.query(Sentence).all()

def get_sentence_from_recording(recording: Recording, session) -> Sentence:
    return session.query(Sentence).filter(Sentence.id == recording.sentence_id).first()

def add_recording(recording, session):
    session.add(recording)

def get_recording_by_attributes(recording: Recording, session):
    try:
        return session.query(Recording).filter(Recording.room_id == recording.room_id, Recording.sentence_id == recording.sentence_id, Recording.conditions_id == recording.conditions_id, Recording.repetition == recording.repetition, Recording.rec_repetition == recording.rec_repetition).first()
    except:
        return None 
    
def get_all_recordings(session):
    return session.query(Recording).all()

def add_new_user(first_name: str, last_name: str, birth_date: datetime):
    user = User(first_name, last_name, birth_date)
    add_to_db(user)

def add_to_db(object, session):
    try:
        session.add(object)
        session.commit()
    except Exception as e:
        print(f'cant add {object}')
        print(e)
    finally:
        session.close()

def get_full_content(table, session):
    results = session.query(table).all()
    return results