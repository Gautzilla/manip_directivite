from view.app_view import AppView
from model.ratings_model import get_next_recording_id, get_recording_filename, write_ratings

class RatingsController():

    def __init__(self, app_controller, app_view: AppView, user_id: int):
        self.app_controller = app_controller
        self.app_view = app_view
        self.user_id = user_id

        self.load_next_recording()
        self.ratings_view = self.app_view.show_ratings(controller = self)

    def load_next_recording(self):
        self.recording_id = get_next_recording_id(user_id = self.user_id)
        self.recording_filename = get_recording_filename(id = self.recording_id)

    def register_rating(self, ratings: tuple):
        write_ratings(ratings, self.user_id, self.recording_id)
        print(f'User {self.user_id} recording {self.recording_id}: {' '.join([str(rating) for rating in ratings])}')
        self.load_next_recording()
