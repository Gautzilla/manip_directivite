from view.app_view import AppView
from model.ratings_model import get_next_recording_id, get_recording_filename, write_ratings, get_progress
from model.audio_player_model import get_sound_duration, play_sound

class RatingsController():

    def __init__(self, app_controller, app_view: AppView, user_id: int):
        self.app_controller = app_controller
        self.app_view = app_view
        self.user_id = user_id
        
        self.ratings_view = self.app_view.show_ratings(controller = self)
        self.load_next_recording()

    def load_next_recording(self):
        self.recording_id = get_next_recording_id(user_id = self.user_id)
        if self.recording_id == None:
            self.app_controller.end_test()
            return
        self.recording_filename = get_recording_filename(id = self.recording_id)
        self.play_next_recording()

    def play_next_recording(self):
        #TODO: remove next line when the correct audios will be added
        self.recording_filename = r'C:\Users\labsticc\Desktop\pink_noise.wav'

        try:            
            recording_duration = get_sound_duration(path = self.recording_filename)
            play_sound(self.recording_filename)
            self.ratings_view.reset_sliders()
            self.ratings_view.disable_validate_button(recording_duration)
            self.update_progress()
        except Exception as e:
            self.ratings_view.display_soundfile_error(soundfile = self.recording_filename)

    def update_progress(self):
        progress = get_progress(self.user_id)
        self.ratings_view.set_progress(progress)

    def register_rating(self, ratings: tuple):
        write_ratings(ratings, self.user_id, self.recording_id)
        self.load_next_recording()
