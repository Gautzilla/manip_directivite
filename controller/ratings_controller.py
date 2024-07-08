from view.app_view import AppView
from model.ratings_model import filter_recordings, get_next_recording_id, get_recording_filename, write_ratings, get_progress
from model.audio_player_model import get_sound_duration, play_sound
from os import path

class RatingsController():

    MEDIA_FOLDER = path.abspath(r'data\audio')

    def __init__(self, app_controller, app_view: AppView, user_id: int):
        self.app_controller = app_controller
        self.app_view = app_view
        self.user_id = user_id

        filter_recordings(rooms = [0,1], distances = [1,4], angles = ['Front','Side'], movements = [0,1], sources = ['Human','Loudspeaker'], amplitudes = ['Small','Large'])
        
        self.ratings_view = self.app_view.show_ratings(controller = self)
        self.app_view.set_binding('<Return>', lambda _ : self.ratings_view.validate())
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
        # self.recording_filename = r'C:\Users\labsticc\Desktop\pink_noise.wav'
        file = path.join(self.MEDIA_FOLDER, self.recording_filename)

        try:            
            recording_duration = get_sound_duration(path = file)
            play_sound(file)
            self.ratings_view.reset_sliders()
            self.ratings_view.disable_validate_button(recording_duration)
            self.update_progress()
        except Exception as e:
            self.ratings_view.display_soundfile_error(soundfile = file)

    def update_progress(self):
        progress = get_progress(self.user_id)
        self.ratings_view.set_progress(progress)

    def register_rating(self, ratings: tuple):
        write_ratings(ratings, self.user_id, self.recording_id)
        self.load_next_recording()
