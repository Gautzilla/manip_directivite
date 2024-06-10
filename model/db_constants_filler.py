from model.models import Room, Condition, Sentence
from data.independant_variables import Source, Distance, Angle
from model.queries import add_conditions, add_room, get_sentence_by_attributes, add_sentence, get_room_by_attributes, get_conditions_by_attributes
from itertools import product
import pandas as pd
from model import Session

SENTENCES_CSV_FILE = r'data\sentences.csv'

def initialize_db():

    #Rooms
    rooms = [Room(0, 'CLOUS', 0.5), Room(1, 'SUAPS', 2.)]

    #Recordings
    recordings = pd.read_csv(SENTENCES_CSV_FILE)

    # Conditions
    conditions = []
    for movement in [True, False]:
        for source, distance, angle in product(Source, Distance, Angle):
            condition = Condition(distance = distance.value, angle = angle.value, movement = movement, source = source.value)
            conditions.append(condition)

    # Sentences
    sentences = map(lambda s: Sentence(text = s[0], amplitude = s[1]), set((recording.loc['Phrase'], recording.loc['T']) for recording in [r[1] for r in recordings.iterrows()]))

    with Session() as session:
        
        for room in rooms:
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


