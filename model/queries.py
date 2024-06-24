from model.models import Room, Condition, User, Sentence, Recording, Rating
from sqlalchemy import select, and_

def get_room_from_recording(recording: Recording, session) -> Room:
        return session.query(Room).filter(Room.id == recording.room_id).first()

def get_room_by_attributes(room, session):
    try:
        return session.query(Room).filter(Room.name == room.name, Room.rt_60 == room.rt_60).first()
    except:
        return None    

def add_room(room: Room, session):
    session.add(room)

def get_conditions_by_attributes(condition, session):
    try:
        return session.query(Condition).filter(Condition.distance == condition.distance, Condition.angle == condition.angle, Condition.movement == condition.movement, Condition.source == condition.source).first()
    except:
        return None  

def add_conditions(conditions: Condition, session):
    session.add(conditions)

def get_conditions_from_recording(recording: Recording, session) -> Condition:
    return session.query(Condition).filter(Condition.id == recording.conditions_id).first()

def get_sentence_by_attributes(sentence: Sentence, session) -> Sentence:
    try:
        return session.query(Sentence).filter(Sentence.text == sentence.text, Sentence.amplitude == sentence.amplitude).first()
    except:
        return None 

def add_sentence(sentence: Sentence, session):
    session.add(sentence)

def get_sentence_from_recording(recording: Recording, session) -> Sentence:
    return session.query(Sentence).filter(Sentence.id == recording.sentence_id).first()

def add_recording(recording: Recording, session):
    session.add(recording)

def get_recording_by_attributes(recording: Recording, session) -> Recording:
    try:
        return session.query(Recording).filter(Recording.room_id == recording.room_id, Recording.sentence_id == recording.sentence_id, Recording.conditions_id == recording.conditions_id, Recording.repetition == recording.repetition, Recording.rec_repetition == recording.rec_repetition).first()
    except:
        return None 
    
def get_all_recordings(session) -> list:
    return session.query(Recording).all()

def get_user_by_attributes(user: User, session) -> User:
    try:
        return session.query(User).filter(User.first_name == user.first_name, User.last_name == user.last_name, User.birth_date == user.birth_date).first()
    except:
        return None
    
def get_uncomplete_users(session) -> list:    
    user_ratings_subquery = select(Recording.id).join(Rating, and_(Rating.user_id == User.id, Rating.recording_id == Recording.id))
    unrated_recordings_subquery = select(Recording.id).exists().where(Recording.id.not_in(user_ratings_subquery))
    results = session.query(User).filter(unrated_recordings_subquery).all()

    return results
    
def add_user(user: User, session):
    session.add(user)

def get_completed_ratings_count(user: User, session) -> int:
    return len(session.query(Rating).filter(Rating.user_id == user.id).all())

def get_unrated_recordings(user_id: int, session) -> list:
    rated_recordings_subquery = select(Rating.recording_id).filter(Rating.user_id == user_id)
    unrated_recordings = session.query(Recording).filter(~Recording.id.in_(rated_recordings_subquery)).all()
    return unrated_recordings

def get_recording(id, session) -> Recording:
    return session.query(Recording).filter(Recording.id == id).first()

def write_ratings(rating, session):
    session.add(rating)