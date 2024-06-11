from model.models import Room, Condition, Sentence, Recordings
from data.independant_variables import Source, Distance, Angle
from model.queries import add_conditions, add_room, get_sentence_by_attributes, add_sentence, get_room_by_attributes, get_conditions_by_attributes, add_recording, get_all_recordings, get_recording_by_attributes
from itertools import product
import pandas as pd
from model import Session

SENTENCES_CSV_FILE = r'data\sentences.csv'
RECORDINGS_TO_DUPLICATE_IN_BOTH_ROOMS = [61,141]
RECORDINGS_TO_REJECT = [40, 54, 117, 120]
REJECTED_RECORDINGS_RATIO = 1/3
ROOMS = [Room(0, 'CLOUS', 0.5), Room(1, 'SUAPS', 2.)]

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

    # Recordings : a sentence appears twice in differents conditions: I can't check for duplicates before feeding the db.

    with Session() as session:

        for index, recording in recordings.iterrows():

            # Rejected recording
            if recording.loc['M_r'] == 2:
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
            if recording.loc['ID'] in RECORDINGS_TO_REJECT:
                continue
            if recording.loc['ID'] in RECORDINGS_TO_DUPLICATE_IN_BOTH_ROOMS:
                for conditions_id in [conditions_id_human, conditions_id_loudspeaker]:
                    for room_id in [0,1]:
                        rec = Recordings(room_id, conditions_id, sentence_id, repetition, rec_repetition)
                        if get_recording_by_attributes(rec, session) is not None:
                            continue
                        add_recording(rec, session)
                continue

            room_id = recording.loc['M_r']
            for conditions_id in [conditions_id_human, conditions_id_loudspeaker]:
                rec = Recordings(room_id, conditions_id, sentence_id, repetition, rec_repetition)
                if get_recording_by_attributes(rec, session) is not None:
                    continue
                add_recording(rec, session)

        session.commit()   

def create_trials():
    pass

def initialize_db():
    recordings = pd.read_csv(SENTENCES_CSV_FILE)
    create_constants(recordings)
    create_recordings(recordings)