from src.model import Session
from src.model.queries import filter_recordings_in_session, get_pretest_recording, get_unrated_recordings, get_recording, write_ratings as write_to_db, get_nb_completed_ratings, get_nb_recordings, get_conditions_from_recording
from random import choice
from src.model.models import Rating, Recording, Condition

def filter_recordings(variables: dict) -> None:
    rooms = variables['Room']
    distances = variables['Distance']
    angles = variables['Angle']
    movements = list(map(lambda movement: 1 if movement else 0, variables['Movement']))
    sources = variables['Source']
    amplitudes = variables['Amplitude']
    
    filter_recordings_in_session(rooms, distances, angles, movements, sources, amplitudes)

def get_pretest_recordings() -> list:

    pretest_recordings = []

    with Session() as session:
        pretest_recordings.append(get_pretest_recording(session, room_name = 'CLOUS', sentence_amplitude = 'Small', distance = 1, angle = 'Side', movement = False, source = 'Human'))
        pretest_recordings.append(get_pretest_recording(session, room_name = 'CLOUS', sentence_amplitude = 'Small', distance = 1, angle = 'Front', movement = False, source = 'Loudspeaker'))
        pretest_recordings.append(get_pretest_recording(session, room_name = 'SUAPS', sentence_amplitude = 'Large', distance = 4, angle = 'Side', movement = True, source = 'Loudspeaker'))
        pretest_recordings.append(get_pretest_recording(session, room_name = 'SUAPS', sentence_amplitude = 'Large', distance = 4, angle = 'Front', movement = True, source = 'Human'))
    return pretest_recordings

def get_next_recording(user_id: int) -> Recording:
    with Session() as session:
        unrated_recordings = get_unrated_recordings(user_id, session)
        if not unrated_recordings:
            return None
        else:
            return choice(unrated_recordings)
        
def get_recording_filename(id: int) -> str:
    with Session() as session:
        recording = get_recording(id, session)
        return recording.audio_file
    
def write_ratings(ratings: tuple, answers: dict, user_id: int, recording_id: int):
    timbre, plausibility = ratings
    angle = answers['angle']
    movement = answers['movement']
    r = Rating(plausibility = plausibility, timbre = timbre, angle = angle, movement = movement, user_id = user_id, recording_id = recording_id)
    with Session() as session:
        write_to_db(r, session)
        session.commit()

def get_progress(user_id: int):
    with Session() as session:
        nb_rated_recordings = get_nb_completed_ratings(user_id, session)
        nb_total_recordings = get_nb_recordings(session)
    return nb_rated_recordings / nb_total_recordings

def get_correct_answers_from_recording(recording: Recording) -> dict:
    with Session() as session:
        conditions: Condition = get_conditions_from_recording(recording = recording, session = session)
    return {'angle': conditions.angle, 'movement': conditions.movement}

def check_answers(user_answers: dict, correct_answers: dict) -> dict:
    answers = {}
    for key, value in user_answers.items():
        answers[key] = value == correct_answers[key]
    return answers
