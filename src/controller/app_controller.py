from src.model.app_model import AppModel
from src.view.app_view import AppView
from src.controller.login_controller import LoginController
from src.controller.ratings_controller import TestRatingsController


class AppController():

    def __init__(self):
        self.model = AppModel()
        self.view = AppView(self)

    def initialize_app(self, initialize_db: bool):

        if initialize_db:
            self.model.initialize_db()

        login_controller = LoginController(app_controller = self, app_view = self.view)
        
        self.view.mainloop()
    
    def complete_user_registration(self, user_id: int, variables: dict):
        self.user_id = user_id
        self.view.close_login_view()
        ratings_controller = TestRatingsController(app_controller = self, app_view = self.view, user_id = self.user_id, variables = variables)

    def end_test(self):
        self.view.close_ratings_view()
        self.view.show_test_end()