from model.app_model import AppModel
from view.app_view import AppView
from controller.login_controller import LoginController
from controller.ratings_controller import RatingsController
from model.models import User
from model import Session


class AppController():

    def __init__(self):
        self.model = AppModel()
        self.view = AppView(self)

    def initialize_app(self, initialize_db: bool):

        if initialize_db:
            self.model.initialize_db()

        login_controller = LoginController(app_controller = self, app_view = self.view)
        
        self.view.mainloop()
    
    def complete_user_registration(self, user: User):
        self.view.close_login_view()
        ratings_controller = RatingsController(app_controller = self, app_view = self.view)