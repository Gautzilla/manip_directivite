from src.view.app_view import AppView
from src.model.ratings_model import filter_recordings, get_pretest_recordings, get_next_recording, get_recording_filename, write_ratings, get_progress, get_correct_answers_from_recording, check_answers
from src.model.audio_player_model import get_sound_duration, play_sound
from os import path
from src import AUDIO_FOLDER
from abc import ABC, abstractmethod

class RatingsController(ABC):

    @abstractmethod
    def __init__(self, app_view: AppView):
        self.ratings_view.display_text(text = 'Appuyer sur ENTREE pour démarrer le test.')
        self.app_view.set_binding('<Return>', lambda _ : self.start_test())
        pass

    @abstractmethod
    def start_test(self):
        self.app_view.set_binding('<Return>', lambda _ : self.ratings_view.validate())
        self.ratings_view.display_text(text = '')
        self.load_next_recording()

    @abstractmethod
    def load_next_recording(self):
        if self.recording == None:
            self.app_controller.end_test()
            return
        self.recording_filename = get_recording_filename(id = self.recording.id)
        self.correct_answers = get_correct_answers_from_recording(recording = self.recording) # Facing Angle / Movement
        self.play_next_recording()

    @abstractmethod
    def play_next_recording(self):
        file = path.join(AUDIO_FOLDER, self.recording_filename)

        try:            
            recording_duration = get_sound_duration(path = file)
            play_sound(file)
            self.ratings_view.reset(list(self.correct_answers.keys()))
            self.ratings_view.disable_validate_button(recording_duration)
            self.ratings_view.display_soundfile_name(soundfile = path.basename(file))
            self.update_progress()
        except Exception as e:
            self.ratings_view.display_soundfile_error(soundfile = file)
            raise e

    @abstractmethod
    def update_progress(self):
        pass

class TestRatingsController(RatingsController):
    
    def __init__(self, app_controller, app_view: AppView, user_id: int, variables: dict):
        self.app_controller = app_controller
        self.app_view = app_view
        self.user_id = user_id

        filter_recordings(variables)
        self.ratings_view = self.app_view.show_ratings(controller = self)
        super().__init__(app_view = self.app_view)

    def start_test(self):
        super().start_test()

    def load_next_recording(self):
        self.recording = get_next_recording(user_id = self.user_id)
        super().load_next_recording()

    def play_next_recording(self):
        super().play_next_recording()

    def update_progress(self):
        progress = get_progress(self.user_id)
        self.ratings_view.set_progress(progress)

    def register_rating(self, ratings: tuple, answers: dict):
        result = check_answers(user_answers = answers, correct_answers = self.correct_answers)
        write_ratings(ratings = ratings, answers = result, user_id = self.user_id, recording_id = self.recording.id)
        self.load_next_recording()

class PretestRatingsController(RatingsController):
    
    def __init__(self, app_controller, app_view: AppView):
        self.app_controller = app_controller
        self.app_view = app_view
        self.nb_rated_recordings = 0
        self.recordings = get_pretest_recordings()
        self.ratings_view = self.app_view.show_ratings(controller = self)
        super().__init__(app_view = self.app_view)

    def start_test(self):
        super().start_test()

    def load_next_recording(self):
        if self.nb_rated_recordings >= len(self.recordings):
            self.app_controller.close_pretest()
            return
        self.recording = self.recordings[self.nb_rated_recordings]
        super().load_next_recording()

    def play_next_recording(self):
        super().play_next_recording()

    def update_progress(self):
        progress = self.nb_rated_recordings / len(self.recordings)
        self.ratings_view.set_progress(progress)
        self.nb_rated_recordings += 1

    def register_rating(self, ratings: tuple, answers: dict):
        self.load_next_recording()