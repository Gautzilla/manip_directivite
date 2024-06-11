from model.models import Room, Condition, User, Sentence, IndependantVariables
import datetime

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

def get_sentence_by_attributes(sentence, session):
    try:
        return session.query(Sentence).filter(Sentence.text == sentence.text, Sentence.amplitude == sentence.amplitude).first()
    except:
        return None 

def add_sentence(sentence, session):
    session.add(sentence)

def get_all_sentences(session):
    return session.query(Sentence).all()

def add_independant_variables(independant_variables, session):
    session.add(independant_variables)

def get_independant_variables_by_attributes(independant_variables: IndependantVariables, session):
    try:
        return session.query(IndependantVariables).filter(IndependantVariables.room_id == independant_variables.room_id, IndependantVariables.sentence_id == independant_variables.sentence_id, IndependantVariables.conditions_id == independant_variables.conditions_id).first()
    except:
        return None 
    
def get_all_independant_variables(session):
    return session.query(IndependantVariables).all()

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