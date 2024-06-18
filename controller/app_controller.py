from model.app_model import AppModel
from view.app_view import AppView
from controller.login_controller import LoginController


class AppController():

    def __init__(self):
        self.model = AppModel()
        self.view = AppView(self)

    def initialize_app(self, initialize_db : bool):

        if initialize_db:
            self.model.initialize_db()

        login_controller = LoginController(app_controller = self, app_view = self.view)
        
        self.view.mainloop()
    
    def complete_user_registration(self):
        self.view.show_ratings_view()