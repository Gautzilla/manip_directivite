from model import Session
from model.queries import get_unrated_recordings, get_recording
from random import choice
from model.models import Recording

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