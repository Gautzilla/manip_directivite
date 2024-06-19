from view.app_view import AppView
from model.models import Rating, User
from model.ratings_model import get_next_recording_id, get_recording_filename

class RatingsController():

    def __init__(self, app_controller, app_view: AppView, user_id: int):
        self.app_controller = app_controller
        self.app_view = app_view
        self.user_id = user_id

        self.app_view.show_ratings(controller = self)

    def load_next_recording(self):
        next_recording_id = get_next_recording_id(user_id = self.user_id)
        next_recording_filename = get_recording_filename(id = next_recording_id)