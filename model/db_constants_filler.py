from model.models import Room, Condition, Sentence, Recording
from data.independant_variables import Source, Distance, Angle
from model.queries import *
from itertools import product
import pandas as pd
from model import Session
from os import path

SENTENCES_CSV_FILE = path.abspath('data/sentences.csv')
RECORDINGS_TO_DUPLICATE_IN_BOTH_ROOMS = [61,141, 118, 133, 82, 118, 24]
RECORDINGS_TO_REJECT = [40, 54, 117, 120, 134, 127, 94, 45, 13, 134, 20]
REJECTED_RECORDINGS_RATIO = 1/3
ROOMS = [Room(0, 'CLOUS', 0.5), Room(1, 'SUAPS', 2.)]

def get_variables() -> dict:
    variables = {}

    with Session() as session:
        variables['Room'] = [room.name for room in get_all_rooms(session)]
        variables['Distance'] = [distance[0] for distance in get_all_distances(session)]
        variables['Angle'] = [angle[0] for angle in get_all_angles(session)]
        variables['Movement'] = [movement[0] for movement in get_all_movements(session)]
        variables['Source'] = [source[0] for source in get_all_sources(session)]
        variables['Amplitude'] = [amplitude[0] for amplitude in get_all_amplitudes(session)]

    return variables

def create_constants(recordings: pd.DataFrame):
    # Conditions
    conditions = []
    for movement in [True, False]:
        for source, distance, angle in product(Source, Distance, Angle):
            condition = Condition(distance = distance.value, angle = angle.value, movement = movement, source = source.value)
            conditions.append(condition)

    # Sentences
    sentences = map(lambda s: Sentence(text = s[0], amplitude = s[1]), set((recording.loc['Phrase'], recording.loc['T']) for recording in [r[1] for r in recordings.iterrows()]))

    with Session() as session:
        
        for room in ROOMS:
            if get_room_by_attributes(room, session) is not None:
                continue
            add_room(room, session)

        for condition in conditions:
            if get_conditions_by_attributes(condition, session) is not None:
                continue
            add_conditions(condition,session)

        for sentence in sentences:
            if get_sentence_by_attributes(sentence, session) is not None:
                continue
            add_sentence(sentence, session)

        session.commit()

def create_recordings(recordings: pd.DataFrame):
    
    with Session() as session:

        for index, recording in recordings.iterrows():

            id = recording.loc['ID']
            rec_room_attribution = recording.loc['M_r'] # 0: Clous, 1: Suaps, 2: Rejected

            # Rejected recording
            if rec_room_attribution == 2:
                continue

            if id in RECORDINGS_TO_REJECT:
                continue

            # Get corresponding IDs in the db
            text = recording.loc['Phrase']
            amplitude = recording.loc['T']
            distance = 1 if recording.loc['D'] == 'Close' else 4
            angle = recording.loc['A']
            movement = recording.loc['M']
            repetition = recording.loc['N']
            rec_repetition = recording.loc['Rec_N']
            sentence_id = get_sentence_by_attributes(Sentence(text = text, amplitude = amplitude), session).id
            conditions_id_human = get_conditions_by_attributes(Condition(distance = distance, angle = angle, movement = movement, source = 'Human'), session).id
            conditions_id_loudspeaker = get_conditions_by_attributes(Condition(distance = distance, angle = angle, movement = movement, source = 'Loudspeaker'), session).id

            # Special cases:            
            if id in RECORDINGS_TO_DUPLICATE_IN_BOTH_ROOMS:
                for conditions_id in [conditions_id_human, conditions_id_loudspeaker]:
                    for room_id in [0,1]:
                        rec = Recording(room_id, conditions_id, sentence_id, repetition, rec_repetition, rec_room_attribution)
                        if get_recording_by_attributes(rec, session) is not None:
                            continue
                        add_recording(rec, session)
                continue
            
            for conditions_id in [conditions_id_human, conditions_id_loudspeaker]:
                rec = Recording(rec_room_attribution, conditions_id, sentence_id, repetition, rec_repetition, rec_room_attribution)
                if get_recording_by_attributes(rec, session) is not None:
                    continue
                add_recording(rec, session)

        session.commit()   

def add_audio_file_names():
    with Session() as session:
        for recording in get_all_recordings(session):
            room = get_room_from_recording(recording, session).name
            conditions = get_conditions_from_recording(recording, session)
            source = conditions.source
            distance = 'Close' if conditions.distance == 1 else 'Far'
            angle = conditions.angle
            movement = 'True' if conditions.movement else 'False'
            repetition = str(recording.repetition)
            rec_repetition = str(recording.rec_repetition)
            rec_repetition_rating = str(recording.rec_repetition_rating)
            sentence = get_sentence_from_recording(recording, session)
            amplitude = sentence.amplitude

            audio_file_name = '_'.join(['KU100', room, source, distance, angle, movement, repetition, rec_repetition, amplitude, rec_repetition_rating]) + '.wav'
            recording.set_audio_file(audio_file_name)

        session.commit()

def initialize_db():
    recordings = pd.read_csv(SENTENCES_CSV_FILE)
    create_constants(recordings)
    create_recordings(recordings)
    add_audio_file_names()