from model.models import Room, Condition, User, Sentence
import datetime

def get_room_by_attributes(room, session):
    try:
        return session.query(Room).filter(Room.name == room.name, Room.rt_60 == room.rt_60).first()
    except:
        return None    

def add_room(room, session):
    session.add(room)

def get_conditions_by_attributes(condition, session):
    try:
        return session.query(Condition).filter(Condition.distance == condition.distance, Condition.angle == condition.angle, Condition.movement == condition.movement, Condition.source == condition.source).first()
    except:
        return None  

def add_conditions(conditions, session):
    session.add(conditions)

def get_sentence_by_attributes(sentence, session):
    try:
        return session.query(Sentence).filter(Sentence.text == sentence.text, Sentence.amplitude == sentence.amplitude).first()
    except:
        return None 

def add_sentence(sentence, session):
    session.add(sentence)

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