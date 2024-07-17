from src.model.models import Room, Condition, User, Sentence, Recording, Rating
from sqlalchemy import select, and_

JOINED_TABLES = select(Recording.id).join(Room, Room.id == Recording.room_id).join(Condition, Condition.id == Recording.conditions_id).join(Sentence, Sentence.id == Recording.sentence_id)
_recordings_in_session = JOINED_TABLES # filtered by filter_recordings_in_session function

def filter_recordings_in_session(rooms: list, distances: list, angles: list, movements: list, sources: list, amplitudes: list):
    global _recordings_in_session
    _recordings_in_session = JOINED_TABLES.filter(
        Room.name.in_(rooms)
    ).filter(
        and_(Condition.angle.in_(angles), Condition.distance.in_(distances), Condition.movement.in_(movements), Condition.source.in_(sources))
    ).filter(
        Sentence.amplitude.in_(amplitudes)
    )

def get_room_from_recording(recording: Recording, session) -> Room:
    return session.query(Room).filter(Room.id == recording.room_id).first()

def get_room_by_attributes(room, session):
    try:
        return session.query(Room).filter(Room.name == room.name, Room.rt_60 == room.rt_60).first()
    except:
        return None   

def get_all_rooms(session):
    return session.query(Room).all()

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

def get_all_distances(session) -> list:
    return session.query(Condition.distance).distinct()

def get_all_movements(session) -> list:
    return session.query(Condition.movement).distinct()

def get_all_angles(session) -> list:
    return session.query(Condition.angle).distinct()

def get_all_sources(session) -> list:
    return session.query(Condition.source).distinct()

def get_all_amplitudes(session) -> list:
    return session.query(Sentence.amplitude).distinct()

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
    user_ratings_subquery = _recordings_in_session.join(Rating, and_(Rating.user_id == User.id, Rating.recording_id == Recording.id))
    unrated_recordings_subquery = _recordings_in_session.exists().where(Recording.id.not_in(user_ratings_subquery))
    results = session.query(User).filter(unrated_recordings_subquery).all()

    return results
    
def add_user(user: User, session):
    session.add(user)

def get_nb_completed_ratings(user_id: int, session) -> int:
    return len(session.query(Rating.id).filter(Rating.user_id == user_id).all())

def get_nb_recordings(session) -> int:
    return len(session.query(_recordings_in_session.subquery()).all())

def get_unrated_recordings(user_id: int, session) -> list:
    rated_recordings_subquery = select(Rating.recording_id).filter(Rating.user_id == user_id)
    unrated_recordings = session.query(Recording).where(and_(Recording.id.in_(_recordings_in_session), ~Recording.id.in_(rated_recordings_subquery))).all()
    return unrated_recordings

def get_recording(id, session) -> Recording:
    return session.query(Recording).filter(Recording.id == id).first()

def write_ratings(rating, session):
    session.add(rating)