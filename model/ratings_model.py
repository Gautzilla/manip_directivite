from model import Session
from model.queries import filter_recordings_in_session, get_unrated_recordings, get_recording, write_ratings as write_to_db, get_nb_completed_ratings, get_nb_recordings
from random import choice
from model.models import Rating

def filter_recordings(variables: dict) -> None:
    rooms = variables['Room']
    distances = variables['Distance']
    angles = variables['Angle']
    movements = list(map(lambda movement: 1 if movement else 0, variables['Movement']))
    sources = variables['Source']
    amplitudes = variables['Amplitude']
    
    filter_recordings_in_session(rooms, distances, angles, movements, sources, amplitudes)

def get_next_recording_id(user_id: int) -> int:
    with Session() as session:
        unrated_recordings = get_unrated_recordings(user_id, session)
        if not unrated_recordings:
            return None
        else:
            return choice(unrated_recordings).id
        
def get_recording_filename(id: int) -> str:
    with Session() as session:
        recording = get_recording(id, session)
        return recording.audio_file
    
def write_ratings(ratings: tuple, user_id: int, recording_id: int):
    timbre, source_width, plausibility = ratings
    r = Rating(plausibility = plausibility, source_width = source_width, timbre = timbre, user_id = user_id, recording_id = recording_id)
    with Session() as session:
        write_to_db(r, session)
        session.commit()

def get_progress(user_id: int):
    with Session() as session:
        nb_rated_recordings = get_nb_completed_ratings(user_id, session)
        nb_total_recordings = get_nb_recordings(session)
    return nb_rated_recordings / nb_total_recordings